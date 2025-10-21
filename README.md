# EPD_Hangul

GxEPD2 전자잉크 디스플레이에서 한글을 쉽게 표현하기 위한 라이브러리

## 프로젝트 목적

[GxEPD2](https://github.com/ZinggJM/GxEPD2) 라이브러리를 사용하는 전자잉크 디스플레이에서 한글 폰트를 쉽게 작성하고 사용할 수 있도록 지원합니다.

## 주요 기능

- **AimHangul 라이브러리**: 전자잉크 디스플레이에서 한글 표시
- **옛한글 텍스트 뷰어 폰트**: EasyView 프로그램의 폰트 데이터 활용
- **다양한 크기 지원**: 기본, 2배, 4배 확대 표시

## 사용 방법

```cpp
#include <GxEPD2_BW.h>
#include <AimHangul_EPD.h>

GxEPD2_BW<GxEPD2_154, GxEPD2_154::HEIGHT> display(GxEPD2_154(/*CS*/ SS, /*DC*/ 8, /*RST*/ 9, /*BUSY*/ 7));

void setup() {
  display.init();
  display.setRotation(1);
  display.setFullWindow();
  display.firstPage();
  
  do {
    display.fillScreen(GxEPD_WHITE);
    AimHangul(10, 30, "안녕하세요", GxEPD_BLACK);
  } while (display.nextPage());
}
```

### 주요 함수

- `AimHangul(x, y, text, color)` - 기본 크기로 한글 표시
- `AimHangul_h2(x, y, text, color)` - 가로 2배 확대
- `AimHangul_v2(x, y, text, color)` - 세로 2배 확대
- `AimHangul_x4(x, y, text, color)` - 가로/세로 4배 확대

## 폰트 정보

옛한글 텍스트 뷰어(EasyView)의 폰트 파일을 활용하여 완성도 높은 한글 표현이 가능합니다.

- 한글 폰트: `KSFont.h`
- ASCII 폰트: `ASCFont.h`

## 라이브러리 구조

```
AimHangul/
├── AimHangul_EPD.h   # GxEPD2용 한글 라이브러리 (전자잉크 디스플레이)
├── AimHangul_TFT.h   # TFT LCD용 한글 라이브러리 (M5Stack, TFT_eSPI 등)
├── KSFont.h          # 한글 폰트 데이터
├── ASCFont.h         # ASCII 폰트 데이터
└── fonts/            # 변환된 폰트 헤더 파일들

tools/
├── han_font_converter.py   # 한글 폰트 변환 도구 (.han → .h)
├── test_hangul_font.py     # 폰트 테스트 및 시각화
├── requirements.txt        # Python 의존성
└── README.md              # 도구 사용 설명서
```

## 한글 폰트 변환 도구

EasyView의 `.han` 폰트 파일을 Arduino용 `.h` 파일로 변환할 수 있습니다.

### 설치

```powershell
cd tools
pip install -r requirements.txt
```

### 사용법

**모든 폰트 변환:**
```powershell
python han_font_converter.py
```

**변환된 폰트 테스트:**
```powershell
python test_hangul_font.py "../AimHangul/fonts/H01.h" --text "안녕하세요"
```

자세한 사용법은 [tools/README.md](tools/README.md)를 참조하세요.

## 참고 자료

- [GxEPD2 한글 표시 방법](https://blog.naver.com/sanguru/221854830624)
- [전자책 프로젝트 - 한글 폰트](https://blog.naver.com/gilchida/222927710968)
- [옛한글 텍스트 뷰어 EasyView](한글%20디스플레이%20관련자료/EasyView-3.0.b2/)

