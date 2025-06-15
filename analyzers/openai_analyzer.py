#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI 기반 텍스트 분석기 - 디버깅 강화 버전
"""

import openai
import logging

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class OpenAIAnalyzer:
    """OpenAI API를 사용한 자살유발정보 분석기"""

    def __init__(self, config):
        """OpenAI 분석기 초기화"""
        self.config = config

        # API 키 상태 상세 로깅
        if config.has_openai_config():
            api_key = config.openai_api_key
            logger.info(f"OpenAI API 키 감지됨: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else ''}")

            try:
                self.client = openai.OpenAI(api_key=config.openai_api_key)
                logger.info("OpenAI 클라이언트 초기화 성공")

                # API 연결 테스트
                self._test_connection()

            except Exception as e:
                logger.error(f"OpenAI 클라이언트 초기화 실패: {e}")
                self.client = None
        else:
            logger.warning("OpenAI API 키가 설정되지 않음")
            self.client = None

    def _test_connection(self):
        """OpenAI API 연결 테스트"""
        try:
            test_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            logger.info("OpenAI API 연결 테스트 성공")
            return True
        except Exception as e:
            logger.error(f"OpenAI API 연결 테스트 실패: {e}")
            self.client = None
            return False

    def analyze(self, text):
        """텍스트 분석"""
        logger.debug(f"분석 시작 - 텍스트 길이: {len(text)}자")

        if not self.client:
            logger.warning("OpenAI 클라이언트가 없음 - 예외 발생")
            raise Exception("OpenAI API 설정이 없습니다.")

        prompt = self._create_analysis_prompt(text)
        logger.debug(f"프롬프트 생성 완료 - 길이: {len(prompt)}자")

        try:
            logger.info("OpenAI API 호출 시작...")

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.1
            )

            result = response.choices[0].message.content

            # 강화된 응답 로깅
            print("=" * 50)
            print("OpenAI API 응답:")
            print(result)
            print("=" * 50)

            logger.info("OpenAI API 호출 성공")
            logger.debug(f"응답 내용: {result}")

            parsed_result = self._parse_result(result)
            logger.debug(f"파싱 결과: {parsed_result}")

            return parsed_result

        except openai.AuthenticationError as e:
            logger.error(f"OpenAI 인증 오류: {e}")
            raise Exception(f"OpenAI 인증 실패: API 키를 확인해주세요")
        except openai.RateLimitError as e:
            logger.error(f"OpenAI 요청 한도 초과: {e}")
            raise Exception(f"OpenAI 요청 한도 초과: 잠시 후 다시 시도해주세요")
        except openai.APIError as e:
            logger.error(f"OpenAI API 오류: {e}")
            raise Exception(f"OpenAI API 오류: {e}")
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}")
            raise Exception(f"OpenAI 분석 중 오류: {e}")

    def _create_analysis_prompt(self, text):
        """분석 프롬프트 생성"""
        return f"""
다음 텍스트가 자살유발정보에 해당하는지 분석해주세요.

자살유발정보 판단 기준:
1. 자살동반자 모집정보
2. 자살에 대한 구체적인 방법을 제시하는 정보
3. 자살을 실행하거나 유도하는 내용을 담은 정보
4. 자살위해물건의 판매 또는 활용에 관한 정보

분석할 텍스트:
{text[:500]}

다음 형식으로 정확히 응답해주세요:
위험도: [0.0-1.0 사이의 숫자]
판정: [Y 또는 N]
근거: [구체적인 판단 근거]
"""

    def _parse_result(self, result):
        """결과 파싱 - 개선된 버전"""
        logger.debug(f"파싱 시작: {result}")

        lines = result.split('\n')
        risk_score = 0.0
        is_risky = 'N'
        reason = ''

        for line in lines:
            line = line.strip()
            logger.debug(f"파싱 중인 라인: {line}")

            if '위험도:' in line or '위험도 :' in line:
                try:
                    # 콜론 이후의 텍스트에서 숫자 추출
                    score_text = line.split(':')[1].strip()
                    risk_score = float(score_text)
                    logger.debug(f"위험도 파싱 성공: {risk_score}")
                except (ValueError, IndexError) as e:
                    logger.warning(f"위험도 파싱 실패: {line}, 오류: {e}")

            elif '판정:' in line or '판정 :' in line:
                try:
                    judgment_text = line.split(':')[1].strip()
                    is_risky = judgment_text.upper()
                    logger.debug(f"판정 파싱 성공: {is_risky}")
                except IndexError as e:
                    logger.warning(f"판정 파싱 실패: {line}, 오류: {e}")

            elif '근거:' in line or '근거 :' in line:
                try:
                    reason_text = line.split(':')[1].strip()
                    reason = reason_text
                    logger.debug(f"근거 파싱 성공: {reason}")
                except IndexError as e:
                    logger.warning(f"근거 파싱 실패: {line}, 오류: {e}")

        logger.info(f"최종 파싱 결과 - 위험도: {risk_score}, 판정: {is_risky}, 근거: {reason}")
        return risk_score, is_risky, reason

    def is_available(self):
        """OpenAI API 사용 가능 여부 확인"""
        return self.client is not None
