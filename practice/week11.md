# Week 11 실습

## 오늘 한 것
- PyInstaller를 설치하고 버전을 확인했다.
- 오니 캠퍼스 게임 파일을 exe 파일로 빌드했다.
- resource_path() 함수를 추가하여 개발 환경과 exe 환경 모두에서 경로가 동작하도록 수정했다.
- --add-data 옵션을 사용해 png, mp3, ttf 파일들을 exe 내부에 포함시켰다.
- 빌드 후 생성된 ONI_CAMPUS_FIXED.exe 파일을 실행해 정상 동작을 확인했다.
- exe 파일을 바탕화면으로 옮긴 뒤에도 게임이 실행되는 것을 확인했다.

## resource_path() 를 써야 하는 이유
PyInstaller의 onefile 방식은 실행 시 임시 폴더에서 프로그램을 실행하기 때문에 상대경로만 사용하면 이미지나 사운드 파일을 찾지 못하는 문제가 발생한다. 이를 해결하기 위해 resource_path() 함수를 사용해 현재 실행 환경에 맞는 경로를 자동으로 찾도록 수정했다.

## 빌드 명령어
pyinstaller --onefile --windowed --add-data "start_bg.png;." --add-data "game_bg.png;." --add-data "characters.png;." --add-data "title_oni.png;." --add-data "oni_awake.png;." --add-data "*.ttf;." --add-data "*.mp3;." --name="ONI_CAMPUS_FIXED" onidae_FIXED.py

## AI 활용 내역
- PyInstaller 실행 오류 원인 분석 도움
- resource_path() 함수 적용 방법 설명
- --add-data 옵션 사용 방법 확인
- exe 실행 오류 디버깅 과정 도움
