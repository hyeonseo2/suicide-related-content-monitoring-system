#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
데이터 모델 정의
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PostData:
    """게시글 데이터 모델"""
    platform: str
    url: str
    title: str
    content: str
    keyword: str
    created_at: Optional[datetime] = None
    crawl_success: bool = True


@dataclass
class AnalysisResult:
    """분석 결과 데이터 모델"""
    risk_score: float
    is_risky: str  # 'Y' or 'N'
    reason: str


@dataclass
class MonitoringResult:
    """모니터링 결과 데이터 모델"""
    post_data: PostData
    analysis_result: AnalysisResult
    collected_at: datetime
