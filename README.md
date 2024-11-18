# 2024-02-CSC4004-3-4-NoGame_back

벡 엔드용 레포지토리입니다.

11/17 12:00 카카오 API에서 유저ID/유저이름/유저사진 정보 가져오기를 PolicyUser에 구현
            실행 시 Kakao 로그인 화면이 뜨며, 로그인 성공 시 Django Resful Framework에 유저 정보가 노출
            이 외의 기능은 구현하지 않았으므로 kakaoRollback/Get/f5 버튼을 누르면 에러 발생
            유저정보를 참조하려면 PolicyUser의 model에 있는 user class를 User.objects.get() 함수 따위를 사용하여 참조

            논의 필요:
            카카오에서 사업자등록을 하지 않으면 상세 정보를 주지 않기에 클래스에 변수만 구현 해놓은 상태
            상세 정보 수기 입력은 아직 구현하지 않았고, 추후 논의에 따라 개발 예정
            
