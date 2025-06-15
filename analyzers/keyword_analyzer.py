#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
키워드 기반 텍스트 분석기
"""


class KeywordAnalyzer:
    """키워드 기반 자살유발정보 분석기"""

    def __init__(self):
        """키워드 분석기 초기화"""
        self.suicide_keywords = [
            '자살', '죽고싶', '자해', '목숨', '극단적선택', '생을마감',
            '죽는방법', '자살방법', '동반자살', '투신', '목매기',
            '자살사이트', '자살카페', '같이죽', '함께죽', '자살동반',
            '우울', '절망', '포기', '의미없', '힘들', '괴로'
        ]

        self.high_risk_keywords = [
            '자살방법', '동반자살', '같이죽', '함께죽', '자살동반',
            '죽는방법', '자살카페', '자살사이트', '자살도구'
        ]

    def analyze(self, text):
        """텍스트 분석"""
        text_lower = text.lower()
        risk_score = 0.0
        found_keywords = []

        for keyword in self.suicide_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
                if keyword in self.high_risk_keywords:
                    risk_score += 0.4
                else:
                    risk_score += 0.1

        risk_score = min(risk_score, 1.0)
        is_risky = 'Y' if risk_score >= 0.3 else 'N'
        reason = f"감지된 키워드: {', '.join(found_keywords)}" if found_keywords else "위험 키워드 미감지"

        return risk_score, is_risky, reason
