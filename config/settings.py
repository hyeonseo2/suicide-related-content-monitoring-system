#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
설정 관리 모듈 - 환경변수 우선순위 강제 적용
"""

import os
from dotenv import load_dotenv


class Config:
    """시스템 설정 관리 클래스"""

    def __init__(self):
        """설정 초기화 - .env 파일 우선순위 적용"""
        # .env 파일의 값이 시스템 환경변수보다 우선하도록 설정
        load_dotenv(override=True)

        # 환경변수 확인 및 디버깅
        self._debug_environment_variables()

        # API 키 로드
        self.twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        self.naver_client_id = os.getenv("NAVER_CLIENT_ID")
        self.naver_client_secret = os.getenv("NAVER_CLIENT_SECRET")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # 크롤링 설정
        self.max_results_per_platform = 50
        self.request_delay = 1.5
        self.timeout = 10

        # 분석 설정
        self.risk_threshold = 0.3
        self.content_max_length = 1000

        # 파일 설정
        self.output_dir = "results"
        self.log_dir = "logs"

        # 플랫폼별 설정
        self.platform_config = {
            'twitter': {
                'max_results': 100,
                'enabled': self.has_twitter_config()
            },
            'naver': {
                'max_results': 50,
                'enabled': self.has_naver_config()
            },
            'dcinside': {
                'max_results': 30,
                'enabled': True
            }
        }

        # 설정 검증
        self.validate_config()

    def _debug_environment_variables(self):
        """환경변수 디버깅 정보 출력"""
        print("=" * 60)
        print("환경변수 로딩 상태 확인")
        print("=" * 60)

        # .env 파일 존재 여부 확인
        env_file_exists = os.path.exists('.env')
        print(f".env 파일 존재: {'예' if env_file_exists else '아니오'}")

        if env_file_exists:
            try:
                with open('.env', 'r', encoding='utf-8') as f:
                    env_content = f.read()
                    has_openai_key = 'OPENAI_API_KEY' in env_content
                    print(f".env 파일에 OPENAI_API_KEY 존재: {'예' if has_openai_key else '아니오'}")
            except Exception as e:
                print(f".env 파일 읽기 오류: {e}")

        # 환경변수 확인
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print(f"사용 중인 API 키: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else ''}")
            print(f"API 키 형식 검증: {'올바름' if api_key.startswith('sk-') else '잘못된 형식 (sk-로 시작해야 함)'}")
        else:
            print("OPENAI_API_KEY 환경변수가 설정되지 않음")

        print("=" * 60)

    def validate_config(self):
        """설정 유효성 검사"""
        missing_keys = []
        invalid_keys = []

        # Twitter API 키 검증
        if not self.twitter_bearer_token:
            missing_keys.append("TWITTER_BEARER_TOKEN")

        # 네이버 API 키 검증
        if not self.naver_client_id or not self.naver_client_secret:
            missing_keys.append("NAVER_API_KEYS")

        # OpenAI API 키 검증
        if not self.openai_api_key:
            missing_keys.append("OPENAI_API_KEY")
        elif not self.openai_api_key.startswith('sk-'):
            invalid_keys.append(f"OPENAI_API_KEY (현재: {self.openai_api_key[:10]}..., 올바른 형식: sk-로 시작)")

        # 경고 메시지 출력
        if missing_keys:
            print(f"⚠️ 누락된 API 키: {', '.join(missing_keys)}")
            print("해당 플랫폼의 데이터 수집이 제한될 수 있습니다.")

        if invalid_keys:
            print(f"❌ 잘못된 형식의 API 키: {', '.join(invalid_keys)}")
            print("OpenAI API 키는 반드시 'sk-'로 시작해야 합니다.")

    def has_twitter_config(self):
        """Twitter API 설정 여부 확인"""
        return bool(self.twitter_bearer_token)

    def has_naver_config(self):
        """네이버 API 설정 여부 확인"""
        return bool(self.naver_client_id and self.naver_client_secret)

    def has_openai_config(self):
        """OpenAI API 설정 여부 확인 - 형식 검증 포함"""
        return bool(self.openai_api_key and self.openai_api_key.startswith('sk-'))

    def get_platform_status(self):
        """모든 플랫폼의 사용 가능 상태 반환"""
        return {
            'twitter': self.has_twitter_config(),
            'naver': self.has_naver_config(),
            'dcinside': True,
            'openai': self.has_openai_config()
        }

    def get_available_platforms(self):
        """사용 가능한 플랫폼 목록 반환"""
        status = self.get_platform_status()
        return [platform for platform, available in status.items() if available and platform != 'openai']

    def print_config_summary(self):
        """설정 요약 정보 출력"""
        print("\n" + "=" * 50)
        print("시스템 설정 요약")
        print("=" * 50)

        status = self.get_platform_status()
        for platform, available in status.items():
            status_text = "✓ 사용 가능" if available else "✗ 사용 불가"
            print(f"{platform.capitalize()}: {status_text}")

        print("=" * 50)
