#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
자살유발정보 모니터링 시스템 - 메인 실행 파일 (플랫폼 선택 기능 추가)
"""

import sys
import os
from datetime import datetime

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from crawlers.twitter_crawler import TwitterCrawler
from crawlers.naver_crawler import NaverCrawler
from crawlers.dcinside_crawler import DCInsideCrawler
from analyzers.openai_analyzer import OpenAIAnalyzer
from analyzers.keyword_analyzer import KeywordAnalyzer
from utils.data_processor import DataProcessor
from utils.file_manager import FileManager


class SuicideMonitoringSystem:
    """자살유발정보 모니터링 시스템 메인 클래스"""

    def __init__(self):
        """시스템 초기화"""
        self.config = Config()
        self.data_processor = DataProcessor()
        self.file_manager = FileManager()

        # 크롤러 초기화
        self.twitter_crawler = TwitterCrawler(self.config)
        self.naver_crawler = NaverCrawler(self.config)
        self.dcinside_crawler = DCInsideCrawler(self.config)

        # 분석기 초기화
        self.openai_analyzer = OpenAIAnalyzer(self.config)
        self.keyword_analyzer = KeywordAnalyzer()

        # 결과 저장 리스트
        self.results = []

        # 선택된 플랫폼 저장
        self.selected_platforms = []

    def get_platform_selection(self):
        """플랫폼 선택 기능"""
        print("\n" + "=" * 50)
        print("데이터 수집 플랫폼 선택")
        print("=" * 50)

        # 사용 가능한 플랫폼 정의
        available_platforms = {
            '1': {
                'name': 'X(Twitter)',
                'description': 'Twitter API를 통한 트윗 수집',
                'available': self.config.has_twitter_config(),
                'crawler': self.twitter_crawler
            },
            '2': {
                'name': '네이버 블로그',
                'description': '네이버 API를 통한 블로그 포스트 수집',
                'available': self.config.has_naver_config(),
                'crawler': self.naver_crawler
            },
            '3': {
                'name': '디시인사이드',
                'description': '크롤링을 통한 게시글 수집',
                'available': True,  # 크롤링은 항상 가능
                'crawler': self.dcinside_crawler
            }
        }

        # 플랫폼 목록 출력
        print("사용 가능한 플랫폼:")
        for key, platform in available_platforms.items():
            status = "✓ 사용 가능" if platform['available'] else "✗ API 키 없음"
            print(f"{key}. {platform['name']} - {platform['description']} ({status})")

        print("\n선택 옵션:")
        print("- 개별 선택: 번호를 쉼표로 구분 (예: 1,2 또는 1,3)")
        print("- 전체 선택: 'all' 또는 'a' 입력")
        print("- 사용 가능한 것만 선택: 'available' 또는 'av' 입력")

        while True:
            selection = input("\n수집할 플랫폼을 선택하세요: ").strip().lower()

            if selection in ['all', 'a']:
                # 전체 선택
                self.selected_platforms = [p for p in available_platforms.values()]
                break
            elif selection in ['available', 'av']:
                # 사용 가능한 것만 선택
                self.selected_platforms = [p for p in available_platforms.values() if p['available']]
                break
            else:
                # 개별 선택
                try:
                    selected_numbers = [num.strip() for num in selection.split(',')]
                    selected_platforms = []

                    for num in selected_numbers:
                        if num in available_platforms:
                            selected_platforms.append(available_platforms[num])
                        else:
                            print(f"잘못된 번호입니다: {num}")
                            break
                    else:
                        # 모든 번호가 유효한 경우
                        self.selected_platforms = selected_platforms
                        break

                except Exception:
                    print("입력 형식이 올바르지 않습니다. 다시 시도해주세요.")

        # 선택된 플랫폼 확인
        if not self.selected_platforms:
            print("선택된 플랫폼이 없습니다.")
            return False

        print(f"\n선택된 플랫폼 ({len(self.selected_platforms)}개):")
        unavailable_count = 0
        for platform in self.selected_platforms:
            if platform['available']:
                print(f"✓ {platform['name']}")
            else:
                print(f"✗ {platform['name']} (API 키 없음 - 건너뜀)")
                unavailable_count += 1

        # 실제 사용 가능한 플랫폼 필터링
        self.selected_platforms = [p for p in self.selected_platforms if p['available']]

        if not self.selected_platforms:
            print("\n모든 선택된 플랫폼이 사용 불가능합니다. API 키를 확인해주세요.")
            return False

        if unavailable_count > 0:
            confirm = input(f"\n사용 불가능한 {unavailable_count}개 플랫폼을 제외하고 계속하시겠습니까? (y/n): ").strip().lower()
            if confirm != 'y':
                return False

        return True

    def get_collection_settings(self):
        """플랫폼별 수집할 게시글 개수 설정"""
        print(f"\n{'=' * 50}")
        print("수집량 설정")
        print("=" * 50)

        # 기본값 설정
        default_counts = {
            'X(Twitter)': 100,
            'Naver Blog': 50,
            'DCInside': 30
        }

        collection_settings = {}

        for platform in self.selected_platforms:
            platform_name = platform['name']
            default_count = default_counts.get(platform_name, 50)

            while True:
                try:
                    user_input = input(f"{platform_name}에서 수집할 게시글 개수 (기본값: {default_count}개, Enter로 기본값 사용): ").strip()

                    if user_input == "":
                        # 기본값 사용
                        count = default_count
                        break
                    else:
                        # 사용자 입력값 검증
                        count = int(user_input)
                        if count <= 0:
                            print("1 이상의 숫자를 입력해주세요.")
                            continue
                        elif count > 1000:
                            confirm = input(f"{count}개는 많은 수량입니다. 계속하시겠습니까? (y/n): ").strip().lower()
                            if confirm != 'y':
                                continue
                        break

                except ValueError:
                    print("숫자만 입력해주세요.")
                    continue

            collection_settings[platform_name] = count
            print(f"✓ {platform_name}: {count}개 설정 완료")

        self.collection_settings = collection_settings
        return True

    def get_user_input(self):
        """사용자 입력 처리 - 수집량 설정 추가"""
        print("=" * 50)
        print("자살유발정보 모니터링 시스템")
        print("=" * 50)

        # 플랫폼 선택
        if not self.get_platform_selection():
            return False

        # 검색 키워드 입력
        print(f"\n{'=' * 50}")
        print("검색 설정")
        print("=" * 50)

        keywords_input = input("검색할 키워드를 입력하세요 (쉼표로 구분): ").strip()
        self.keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]

        if not self.keywords:
            print("키워드를 입력해주세요.")
            return False

        # 모니터링 기간 입력
        print("\n모니터링 기간을 설정하세요:")
        start_date_str = input("시작일 (YYYY-MM-DD): ").strip()
        end_date_str = input("종료일 (YYYY-MM-DD): ").strip()

        try:
            self.start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            self.end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            if self.start_date > self.end_date:
                print("시작일이 종료일보다 늦을 수 없습니다.")
                return False

        except ValueError:
            print("날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 입력해주세요.")
            return False

        # 수집량 설정
        if not self.get_collection_settings():
            return False

        return True

    def collect_data(self):
        """선택된 플랫폼에서 설정된 개수만큼 데이터 수집"""
        print(f"\n선택된 {len(self.selected_platforms)}개 플랫폼에서 데이터 수집을 시작합니다...")
        all_data = []

        for keyword in self.keywords:
            print(f"\n키워드 '{keyword}' 검색 중...")

            for platform in self.selected_platforms:
                platform_name = platform['name']
                count = self.collection_settings.get(platform_name, 50)

                print(f"- {platform_name} 검색 중... (목표: {count}개)")

                try:
                    if platform_name == 'X(Twitter)':
                        data = self.twitter_crawler.search(keyword, self.start_date, self.end_date, max_results=count)
                    elif platform_name == '네이버 블로그':
                        data = self.naver_crawler.search(keyword, max_results=count)
                    elif platform_name == '디시인사이드':
                        data = self.dcinside_crawler.search(keyword, max_results=count)
                    else:
                        data = []

                    all_data.extend(data)
                    print(f"  실제 수집: {len(data)}개")

                except Exception as e:
                    print(f"  {platform_name} 검색 중 오류 발생: {e}")
                    continue

        return all_data

    def analyze_data(self, data):
        """수집된 데이터 분석 - 개선된 오류 처리"""
        print("\n데이터 분석 중...")

        # OpenAI 분석기 사용 가능 여부 확인
        openai_available = self.openai_analyzer.is_available()
        print(f"OpenAI 분석기 상태: {'사용 가능' if openai_available else '사용 불가'}")

        for idx, item in enumerate(data, 1):
            content = item.get('content', '').strip()
            if not content:
                continue

            print(f"분석 중 ({idx}/{len(data)}): {item['platform']} - {item.get('title', '')[:50]}...")

            # 제목과 내용 결합
            combined_text = f"{item.get('title', '')} {content}"

            # 분석 방법 선택
            analysis_method = "미확인"
            try:
                if openai_available:
                    risk_score, is_risky, reason = self.openai_analyzer.analyze(combined_text)
                    analysis_method = "OpenAI"
                else:
                    raise Exception("OpenAI 사용 불가")
            except Exception as e:
                print(f"  OpenAI 분석 실패: {e}")
                print(f"  키워드 분석기로 대체...")
                risk_score, is_risky, reason = self.keyword_analyzer.analyze(combined_text)
                analysis_method = "키워드"

            # 결과 저장
            result = self.data_processor.create_result_record(
                item, risk_score, is_risky, reason
            )
            result['분석방법'] = analysis_method  # 분석 방법 추가
            self.results.append(result)

            if is_risky == 'Y':
                print(f"  ⚠️ 위험 감지: 점수 {risk_score:.2f} (방법: {analysis_method})")

        print(f"분석 완료: {len(self.results)}개 항목이 처리되었습니다.")

    def print_collection_summary(self):
        """수집 요약 정보 출력 - 수집량 정보 추가"""
        print(f"\n{'=' * 50}")
        print("수집 요약")
        print("=" * 50)
        print(f"선택된 플랫폼: {', '.join([p['name'] for p in self.selected_platforms])}")
        print(f"검색 키워드: {', '.join(self.keywords)}")
        print(f"수집 기간: {self.start_date.strftime('%Y-%m-%d')} ~ {self.end_date.strftime('%Y-%m-%d')}")

        print("\n플랫폼별 수집 설정:")
        total_target = 0
        for platform in self.selected_platforms:
            platform_name = platform['name']
            count = self.collection_settings.get(platform_name, 0)
            total_target += count
            print(f"- {platform_name}: {count}개")

        print(f"총 목표 수집량: {total_target}개")
        print("=" * 50)

    def run(self):
        """메인 실행 함수"""
        try:
            print("자살유발정보 모니터링 시스템을 시작합니다.")

            # 사용자 입력 받기
            if not self.get_user_input():
                return

            # 수집 요약 출력
            self.print_collection_summary()

            # 데이터 수집
            collected_data = self.collect_data()
            if not collected_data:
                print("수집된 데이터가 없습니다.")
                return

            print(f"\n총 {len(collected_data)}개의 게시글이 수집되었습니다.")

            # 데이터 분석
            self.analyze_data(collected_data)

            # 결과 저장
            self.file_manager.save_results(self.results)

        except KeyboardInterrupt:
            print("\n사용자에 의해 중단되었습니다.")
        except Exception as e:
            print(f"예상치 못한 오류 발생: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # 리소스 정리
            for platform in self.selected_platforms:
                if platform['name'] == '디시인사이드':
                    self.dcinside_crawler.close()


if __name__ == "__main__":
    system = SuicideMonitoringSystem()
    system.run()
