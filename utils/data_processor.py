#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
데이터 처리 유틸리티
"""

from datetime import datetime


class DataProcessor:
    """데이터 처리 관련 유틸리티"""

    def create_result_record(self, item, risk_score, is_risky, reason):
        """분석 결과 레코드 생성"""
        return {
            '수집일시': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            '플랫폼': item['platform'],
            '게시글_URL': item['url'],
            '게시글_제목': item.get('title', ''),
            '게시글_내용': self._truncate_content(item.get('content', '')),
            'AI_분석_점수': risk_score,
            '자살유발정보_여부': is_risky,
            'AI_분석_근거': reason,
            '검색키워드': item['keyword'],
            '크롤링_성공': item.get('crawl_success', True)
        }

    def _truncate_content(self, content):
        """내용 길이 제한"""
        if len(content) > 500:
            return content[:500] + '...'
        return content

    def calculate_platform_stats(self, results):
        """플랫폼별 통계 계산"""
        platform_stats = {}
        risky_count = 0

        for result in results:
            platform = result['플랫폼']
            if platform not in platform_stats:
                platform_stats[platform] = {'total': 0, 'risky': 0, 'success': 0}

            platform_stats[platform]['total'] += 1

            if result['자살유발정보_여부'] == 'Y':
                platform_stats[platform]['risky'] += 1
                risky_count += 1

            if result.get('크롤링_성공', True):
                platform_stats[platform]['success'] += 1

        return platform_stats, risky_count
