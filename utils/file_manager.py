#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
파일 저장 및 관리 유틸리티
"""

import os
import pandas as pd
from datetime import datetime
from .data_processor import DataProcessor


class FileManager:
    """파일 저장 및 관리"""

    def __init__(self):
        """파일 매니저 초기화"""
        self.data_processor = DataProcessor()
        self._ensure_directories()

    def _ensure_directories(self):
        """필요한 디렉토리 생성"""
        for directory in ['results', 'logs']:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def save_results(self, results, filename=None):
        """결과를 CSV 파일로 저장"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results/suicide_monitoring_result_{timestamp}.csv"

        if not results:
            print("저장할 데이터가 없습니다.")
            return

        # CSV 저장
        df = pd.DataFrame(results)
        df.to_csv(filename, index=False, encoding='utf-8-sig')

        # 통계 출력
        self._print_statistics(results, filename)

    def _print_statistics(self, results, filename):
        """통계 정보 출력"""
        print(f"\n결과가 '{filename}' 파일로 저장되었습니다.")
        print(f"총 {len(results)}개의 게시글이 분석되었습니다.")

        # 플랫폼별 통계
        platform_stats, risky_count = self.data_processor.calculate_platform_stats(results)

        print(f"\n=== 플랫폼별 수집 결과 ===")
        for platform, stats in platform_stats.items():
            success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
            risk_rate = (stats['risky'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"{platform}: {stats['total']}개 수집, 성공률 {success_rate:.1f}%, 위험도 {risk_rate:.1f}%")

        print(f"\n전체 자살유발정보로 판정된 게시글: {risky_count}개")
        if results:
            overall_risk_rate = (risky_count / len(results) * 100)
            print(f"전체 위험도 비율: {overall_risk_rate:.1f}%")
