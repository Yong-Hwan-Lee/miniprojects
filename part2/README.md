# 미니프로젝트 Part2
기간 - 2023.05.02 ~ 2023.05.16

## WPF 학습
- SCADA 시뮬레이션 (SmartHome시스템) 시작
	- C# WPF
	- MahApps.Metro(MetroUI 디자인 라이브러리)
	- Bogus(더미데이터 생성 라이브러리)
	- Newtonsoft.json
	- M2Mqtt (통신 라이브러리)
	- DB 데이터바인딩
	- LiveCharts
	- OxyChart
	
- SmartHome시스템 문제점
	- 실행 후  로그 텍스트박스 내용 많아 UI가 느려짐 - 해결!
	- LiveCharts 대용량 데이터 차트는 무리(LiveCharts v.2 동일)
	- 대용량 데이터 차는 OxyChart를 사용
	
온습도 더미데이터 시뮬레이션

<img src="https://raw.githubusercontent.com/Yong-Hwan-Lee/miniprojects/main/images/smarthome_publisher.gif" width ="520">

스마트홈 모니터링 앱

<img src="https://raw.githubusercontent.com/Yong-Hwan-Lee/miniprojects/main/images/smarthome_monitor.gif" width ="780" >

스마트홈 모니터링 시각화

<img src="https://raw.githubusercontent.com/Yong-Hwan-Lee/miniprojects/main/images/smarthome_monitor2.png" width ="780" >
