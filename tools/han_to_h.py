#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyView 조합형 한글 폰트(.han) to Arduino 헤더 파일(.h) 변환기
"""

import sys
import os
from datetime import datetime

class HangulFontConverter:
    """한글 폰트 변환 클래스"""
    
    # 폰트 구조 상수
    GLYPH_WIDTH = 16
    GLYPH_HEIGHT = 16
    BYTES_PER_GLYPH = 32  # 16행 × 2바이트/행
    
    # 섹션 구성
    CHO_COUNT = 20   # 초성 20자 (맨 앞 비어있음 포함)
    CHO_BUL = 8      # 초성 8벌
    JUNG_COUNT = 22  # 중성 22자 (맨 앞 비어있음 포함)
    JUNG_BUL = 4     # 중성 4벌
    JONG_COUNT = 28  # 종성 28자 (맨 앞 비어있음 포함)
    JONG_BUL = 4     # 종성 4벌
    
    # 오프셋
    CHO_OFFSET = 0
    JUNG_OFFSET = CHO_COUNT * CHO_BUL  # 160
    JONG_OFFSET = JUNG_OFFSET + JUNG_COUNT * JUNG_BUL  # 248
    
    # 총 글리프 수
    TOTAL_GLYPHS = CHO_COUNT * CHO_BUL + JUNG_COUNT * JUNG_BUL + JONG_COUNT * JONG_BUL  # 360
    
    # 예상 파일 크기
    EXPECTED_FILE_SIZE = TOTAL_GLYPHS * BYTES_PER_GLYPH  # 11,520 바이트
    
    # 초성 이름 (인덱스 0은 비어있음)
    CHO_NAMES = [
        "empty", "g", "gg", "n", "d", "dd", "r", "m", "b", "bb",
        "s", "ss", "ng", "j", "jj", "ch", "k", "t", "p", "h"
    ]
    
    # 중성 이름 (인덱스 0은 비어있음, 1도 비어있음)
    JUNG_NAMES = [
        "empty", "empty2", "a", "ae", "ya", "yae", "eo", "e", "yeo", "ye",
        "o", "wa", "wae", "oe", "yo", "u", "wo", "we", "wi", "yu",
        "eu", "ui", "i"
    ]
    
    # 종성 이름 (인덱스 0은 비어있음)
    JONG_NAMES = [
        "empty", "g", "gg", "gs", "n", "nj", "nh", "d", "r", "rg",
        "rm", "rb", "rs", "rt", "rp", "rh", "m", "b", "bs", "s",
        "ss", "ng", "j", "ch", "k", "t", "p", "h"
    ]
    
    def __init__(self, input_file):
        """초기화
        
        Args:
            input_file: 입력 .han 파일 경로
        """
        self.input_file = input_file
        self.font_name = os.path.splitext(os.path.basename(input_file))[0]
        self.font_data = None
        
    def read_font_file(self):
        """폰트 파일 읽기"""
        try:
            with open(self.input_file, 'rb') as f:
                self.font_data = f.read()
            
            if len(self.font_data) != self.EXPECTED_FILE_SIZE:
                print(f"경고: 파일 크기가 예상과 다릅니다. (예상: {self.EXPECTED_FILE_SIZE}, 실제: {len(self.font_data)})")
            
            print(f"폰트 파일 읽기 완료: {len(self.font_data)} 바이트")
            return True
            
        except FileNotFoundError:
            print(f"오류: 파일을 찾을 수 없습니다: {self.input_file}")
            return False
        except Exception as e:
            print(f"오류: 파일 읽기 실패: {e}")
            return False
    
    def get_glyph_data(self, glyph_index):
        """특정 글리프의 데이터 추출
        
        Args:
            glyph_index: 글리프 인덱스 (0~359)
            
        Returns:
            32바이트의 글리프 데이터
        """
        if glyph_index < 0 or glyph_index >= self.TOTAL_GLYPHS:
            return None
        
        offset = glyph_index * self.BYTES_PER_GLYPH
        return self.font_data[offset:offset + self.BYTES_PER_GLYPH]
    
    def format_byte_array(self, data, bytes_per_line=12):
        """바이트 배열을 C 형식으로 포맷팅
        
        Args:
            data: 바이트 데이터
            bytes_per_line: 한 줄당 바이트 수
            
        Returns:
            포맷팅된 문자열
        """
        lines = []
        for i in range(0, len(data), bytes_per_line):
            chunk = data[i:i + bytes_per_line]
            hex_values = ', '.join(f'0x{b:02X}' for b in chunk)
            lines.append(f'  {hex_values}')
        
        return ',\n'.join(lines)
    
    def generate_header_file(self, output_file=None):
        """헤더 파일 생성
        
        Args:
            output_file: 출력 .h 파일 경로 (None이면 자동 생성)
            
        Returns:
            성공 여부
        """
        if self.font_data is None:
            print("오류: 폰트 데이터가 로드되지 않았습니다.")
            return False
        
        if output_file is None:
            output_file = os.path.join(
                os.path.dirname(self.input_file),
                f"{self.font_name}.h"
            )
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # 헤더 주석
                f.write(f"/**\n")
                f.write(f" * {self.font_name} - Korean Hangul Font for Arduino/ESP32\n")
                f.write(f" * \n")
                f.write(f" * Converted from EasyView font file: {os.path.basename(self.input_file)}\n")
                f.write(f" * Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f" * \n")
                f.write(f" * Font Structure:\n")
                f.write(f" * - Glyph Size: {self.GLYPH_WIDTH}x{self.GLYPH_HEIGHT} pixels\n")
                f.write(f" * - Bytes per Glyph: {self.BYTES_PER_GLYPH} bytes\n")
                f.write(f" * - Total Glyphs: {self.TOTAL_GLYPHS}\n")
                f.write(f" * - Total Size: {len(self.font_data)} bytes\n")
                f.write(f" * \n")
                f.write(f" * Glyph Layout:\n")
                f.write(f" * - Cho (초성): {self.CHO_OFFSET}~{self.JUNG_OFFSET-1} ({self.CHO_COUNT} chars x {self.CHO_BUL} bul)\n")
                f.write(f" * - Jung (중성): {self.JUNG_OFFSET}~{self.JONG_OFFSET-1} ({self.JUNG_COUNT} chars x {self.JUNG_BUL} bul)\n")
                f.write(f" * - Jong (종성): {self.JONG_OFFSET}~{self.TOTAL_GLYPHS-1} ({self.JONG_COUNT} chars x {self.JONG_BUL} bul)\n")
                f.write(f" */\n\n")
                
                # Include guard
                guard_name = f"{self.font_name.upper()}_H"
                f.write(f"#ifndef {guard_name}\n")
                f.write(f"#define {guard_name}\n\n")
                
                # Arduino 헤더
                f.write(f"#include <Arduino.h>\n\n")
                
                # 폰트 상수 정의
                f.write(f"// Font constants\n")
                f.write(f"#define {self.font_name.upper()}_WIDTH {self.GLYPH_WIDTH}\n")
                f.write(f"#define {self.font_name.upper()}_HEIGHT {self.GLYPH_HEIGHT}\n")
                f.write(f"#define {self.font_name.upper()}_BYTES_PER_GLYPH {self.BYTES_PER_GLYPH}\n")
                f.write(f"#define {self.font_name.upper()}_TOTAL_GLYPHS {self.TOTAL_GLYPHS}\n\n")
                
                f.write(f"#define {self.font_name.upper()}_CHO_OFFSET {self.CHO_OFFSET}\n")
                f.write(f"#define {self.font_name.upper()}_JUNG_OFFSET {self.JUNG_OFFSET}\n")
                f.write(f"#define {self.font_name.upper()}_JONG_OFFSET {self.JONG_OFFSET}\n\n")
                
                f.write(f"#define {self.font_name.upper()}_CHO_COUNT {self.CHO_COUNT}\n")
                f.write(f"#define {self.font_name.upper()}_CHO_BUL {self.CHO_BUL}\n")
                f.write(f"#define {self.font_name.upper()}_JUNG_COUNT {self.JUNG_COUNT}\n")
                f.write(f"#define {self.font_name.upper()}_JUNG_BUL {self.JUNG_BUL}\n")
                f.write(f"#define {self.font_name.upper()}_JONG_COUNT {self.JONG_COUNT}\n")
                f.write(f"#define {self.font_name.upper()}_JONG_BUL {self.JONG_BUL}\n\n")
                
                # 비트맵 데이터
                f.write(f"// Font bitmap data (MSB first, 16x16 pixels, 32 bytes per glyph)\n")
                f.write(f"const uint8_t {self.font_name}_Bitmaps[] PROGMEM = {{\n")
                
                formatted_data = self.format_byte_array(self.font_data, 12)
                f.write(formatted_data)
                
                f.write(f"\n}};\n\n")
                
                # 글리프 정보 구조체 (추후 확장용)
                f.write(f"// Font info structure\n")
                f.write(f"typedef struct {{\n")
                f.write(f"  const uint8_t *bitmap;      // Pointer to bitmap data\n")
                f.write(f"  uint8_t width;              // Glyph width in pixels\n")
                f.write(f"  uint8_t height;             // Glyph height in pixels\n")
                f.write(f"  uint8_t bytesPerGlyph;      // Bytes per glyph\n")
                f.write(f"  uint16_t totalGlyphs;       // Total number of glyphs\n")
                f.write(f"  uint8_t choOffset;          // Cho section offset\n")
                f.write(f"  uint8_t jungOffset;         // Jung section offset\n")
                f.write(f"  uint16_t jongOffset;        // Jong section offset\n")
                f.write(f"}} HangulFontInfo;\n\n")
                
                f.write(f"// Font info instance\n")
                f.write(f"const HangulFontInfo {self.font_name}_Info PROGMEM = {{\n")
                f.write(f"  {self.font_name}_Bitmaps,\n")
                f.write(f"  {self.GLYPH_WIDTH},\n")
                f.write(f"  {self.GLYPH_HEIGHT},\n")
                f.write(f"  {self.BYTES_PER_GLYPH},\n")
                f.write(f"  {self.TOTAL_GLYPHS},\n")
                f.write(f"  {self.CHO_OFFSET},\n")
                f.write(f"  {self.JUNG_OFFSET},\n")
                f.write(f"  {self.JONG_OFFSET}\n")
                f.write(f"}};\n\n")
                
                # 헬퍼 함수 선언
                f.write(f"// Helper functions\n")
                f.write(f"// Get glyph data by index (0~{self.TOTAL_GLYPHS-1})\n")
                f.write(f"inline const uint8_t* {self.font_name}_getGlyph(uint16_t index) {{\n")
                f.write(f"  if (index >= {self.TOTAL_GLYPHS}) return nullptr;\n")
                f.write(f"  return &{self.font_name}_Bitmaps[index * {self.BYTES_PER_GLYPH}];\n")
                f.write(f"}}\n\n")
                
                f.write(f"// Get cho (초성) glyph by bul and index\n")
                f.write(f"inline const uint8_t* {self.font_name}_getCho(uint8_t bul, uint8_t index) {{\n")
                f.write(f"  if (bul >= {self.CHO_BUL} || index >= {self.CHO_COUNT}) return nullptr;\n")
                f.write(f"  uint16_t glyphIndex = {self.CHO_OFFSET} + bul * {self.CHO_COUNT} + index;\n")
                f.write(f"  return {self.font_name}_getGlyph(glyphIndex);\n")
                f.write(f"}}\n\n")
                
                f.write(f"// Get jung (중성) glyph by bul and index\n")
                f.write(f"inline const uint8_t* {self.font_name}_getJung(uint8_t bul, uint8_t index) {{\n")
                f.write(f"  if (bul >= {self.JUNG_BUL} || index >= {self.JUNG_COUNT}) return nullptr;\n")
                f.write(f"  uint16_t glyphIndex = {self.JUNG_OFFSET} + bul * {self.JUNG_COUNT} + index;\n")
                f.write(f"  return {self.font_name}_getGlyph(glyphIndex);\n")
                f.write(f"}}\n\n")
                
                f.write(f"// Get jong (종성) glyph by bul and index\n")
                f.write(f"inline const uint8_t* {self.font_name}_getJong(uint8_t bul, uint8_t index) {{\n")
                f.write(f"  if (bul >= {self.JONG_BUL} || index >= {self.JONG_COUNT}) return nullptr;\n")
                f.write(f"  uint16_t glyphIndex = {self.JONG_OFFSET} + bul * {self.JONG_COUNT} + index;\n")
                f.write(f"  return {self.font_name}_getGlyph(glyphIndex);\n")
                f.write(f"}}\n\n")
                
                # Include guard 종료
                f.write(f"#endif // {guard_name}\n")
                f.write(f"\n// Approx. {len(self.font_data) + 500} bytes\n")
            
            print(f"헤더 파일 생성 완료: {output_file}")
            print(f"파일 크기: ~{os.path.getsize(output_file)} 바이트")
            return True
            
        except Exception as e:
            print(f"오류: 헤더 파일 생성 실패: {e}")
            return False


def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법: python han_to_h.py <input.han> [output.h]")
        print("예제: python han_to_h.py Apple_kr.han")
        print("      python han_to_h.py Apple_kr.han Apple_kr.h")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"=== 한글 폰트 변환기 ===")
    print(f"입력 파일: {input_file}")
    
    converter = HangulFontConverter(input_file)
    
    # 폰트 파일 읽기
    if not converter.read_font_file():
        sys.exit(1)
    
    # 헤더 파일 생성
    if not converter.generate_header_file(output_file):
        sys.exit(1)
    
    print("\n변환 완료!")


if __name__ == "__main__":
    main()
