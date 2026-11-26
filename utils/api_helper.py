# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 23:41:36 2026

@author: GBC
"""

import json
import requests

try:
    from utils.file_helper import doc_json, luu_json
except ImportError:
    from file_helper import doc_json, luu_json

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OPEN_METEO_GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
DATA_JSON_PATH = "data/data.json"
HEADERS = {
    "User-Agent": "QuanLyTourDuLich_HUIT/1.0 (phuonguyen.student@example.com)",
    "Accept-Language": "vi,en",
}


def _lay_tu_nominatim(tu_khoa, limit, timeout):
    params = {
        "q": tu_khoa,
        "format": "json",
        "addressdetails": 1,
        "limit": limit,
    }
    response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    du_lieu_api = response.json()
    if not isinstance(du_lieu_api, list):
        return []

    ket_qua = []
    for muc in du_lieu_api:
        if not isinstance(muc, dict):
            continue
        dia_chi_obj = muc.get("address") if isinstance(muc.get("address"), dict) else {}
        ten_dia_diem = (
            muc.get("name")
            or dia_chi_obj.get("city")
            or dia_chi_obj.get("town")
            or dia_chi_obj.get("county")
            or tu_khoa
        )
        dia_chi = muc.get("display_name", "")

        toa_do = None
        if muc.get("lat") is not None and muc.get("lon") is not None:
            try:
                toa_do = {"lat": float(muc["lat"]), "lon": float(muc["lon"])}
            except (TypeError, ValueError):
                toa_do = None

        ket_qua.append(
            {
                "tu_khoa": tu_khoa,
                "ten_dia_diem": str(ten_dia_diem).strip(),
                "dia_chi": str(dia_chi).strip(),
                "toa_do": toa_do,
                "nguon": "OpenStreetMap Nominatim API",
            }
        )
    return ket_qua


def _lay_tu_open_meteo(tu_khoa, limit, timeout):
    params = {
        "name": tu_khoa,
        "count": limit,
        "language": "vi",
        "format": "json",
    }
    response = requests.get(OPEN_METEO_GEO_URL, params=params, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    results = payload.get("results") if isinstance(payload, dict) else None
    if not isinstance(results, list):
        return []

    ket_qua = []
    for muc in results:
        if not isinstance(muc, dict):
            continue
        ten_dia_diem = muc.get("name") or tu_khoa
        thanh_phan_dia_chi = [
            str(muc.get(k)).strip()
            for k in ("name", "admin2", "admin1", "country")
            if muc.get(k)
        ]
        dia_chi = ", ".join(dict.fromkeys(thanh_phan_dia_chi))

        toa_do = None
        if muc.get("latitude") is not None and muc.get("longitude") is not None:
            try:
                toa_do = {
                    "lat": float(muc["latitude"]),
                    "lon": float(muc["longitude"]),
                }
            except (TypeError, ValueError):
                toa_do = None

        ket_qua.append(
            {
                "tu_khoa": tu_khoa,
                "ten_dia_diem": str(ten_dia_diem).strip(),
                "dia_chi": dia_chi,
                "toa_do": toa_do,
                "nguon": "Open-Meteo Geocoding API",
            }
        )
    return ket_qua


def lay_du_lieu_diem_den(tu_khoa, limit=5, duong_dan_json=DATA_JSON_PATH, timeout=10):
    """
    Lấy thông tin điểm đến từ API công khai theo từ khóa,
    trích xuất tên địa điểm, địa chỉ, tọa độ và lưu vào danh sách `destinations`
    trong `data/data.json` bằng `doc_json` và `luu_json` của `file_helper.py`.
    Dừng lưu nếu đọc file JSON bị lỗi hoặc lưu thất bại để bảo toàn dữ liệu cũ.
    """
    if not isinstance(tu_khoa, str) or not tu_khoa.strip():
        raise ValueError("Từ khóa tìm kiếm điểm đến không được bỏ trống.")

    tu_khoa_chuan = tu_khoa.strip()
    danh_sach_diem_den = []

    try:
        danh_sach_diem_den = _lay_tu_nominatim(tu_khoa_chuan, limit=limit, timeout=timeout)
    except Exception as loi_nom:
        print(f"Nominatim chưa lấy được dữ liệu cho '{tu_khoa_chuan}' ({loi_nom}), thử nguồn dự phòng...")
        try:
            danh_sach_diem_den = _lay_tu_open_meteo(tu_khoa_chuan, limit=limit, timeout=timeout)
        except Exception as loi_meteo:
            print(f"Lỗi khi lấy dữ liệu điểm đến '{tu_khoa_chuan}': {loi_meteo}")
            return []

    if not danh_sach_diem_den:
        try:
            danh_sach_diem_den = _lay_tu_open_meteo(tu_khoa_chuan, limit=limit, timeout=timeout)
        except Exception:
            pass

    if not danh_sach_diem_den:
        print(f"Không lấy được dữ liệu điểm đến cho từ khóa '{tu_khoa_chuan}'.")
        return []

    try:
        du_lieu_json = doc_json(duong_dan_json, mac_dinh={})
    except (json.JSONDecodeError, OSError) as loi_doc:
        print(f"Không thể đọc file '{duong_dan_json}' ({loi_doc}). Dừng thao tác lưu để bảo toàn dữ liệu cũ.")
        return []

    if du_lieu_json is None:
        du_lieu_json = {}

    if not isinstance(du_lieu_json, dict):
        print(f"Dữ liệu gốc trong '{duong_dan_json}' không phải là dict. Dừng thao tác lưu để bảo toàn dữ liệu cũ.")
        return []

    destinations_cu = du_lieu_json.get("destinations")
    if not isinstance(destinations_cu, list):
        destinations_cu = []

    destinations_moi = list(destinations_cu)
    khoa_da_co = {
        (str(d.get("ten_dia_diem", "")).lower(), str(d.get("dia_chi", "")).lower())
        for d in destinations_moi
        if isinstance(d, dict)
    }

    for dd in danh_sach_diem_den:
        khoa = (dd["ten_dia_diem"].lower(), dd["dia_chi"].lower())
        if khoa not in khoa_da_co:
            destinations_moi.append(dd)
            khoa_da_co.add(khoa)

    du_lieu_json["destinations"] = destinations_moi
    da_luu = luu_json(duong_dan_json, du_lieu_json)
    if not da_luu:
        print(f"Lưu dữ liệu vào '{duong_dan_json}' không thành công (luu_json trả về False).")

    return danh_sach_diem_den


if __name__ == "__main__":
    ket_qua = lay_du_lieu_diem_den("Đà Lạt", limit=3)
    for dd in ket_qua:
        print(dd)