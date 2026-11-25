# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 17:21:12 2026

@author: GBC
"""
import json
import requests

try:
    from utils import file_helper
except ImportError:
    file_helper = None

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OPEN_METEO_GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
DATA_JSON_PATH = "data/data.json"
HEADERS = {
    "User-Agent": "QuanLyTourDuLich_HUIT/1.0 (phuonguyen.student@example.com)",
    "Accept-Language": "vi,en",
}


def _doc_json(duong_dan=DATA_JSON_PATH):
    if file_helper is not None:
        for ten_ham in ("doc_json", "load_json", "read_json"):
            ham = getattr(file_helper, ten_ham, None)
            if callable(ham):
                du_lieu = ham(duong_dan)
                if isinstance(du_lieu, dict):
                    return du_lieu
    try:
        with open(duong_dan, "r", encoding="utf-8") as f:
            du_lieu = json.load(f)
            if isinstance(du_lieu, dict):
                return du_lieu
    except (FileNotFoundError, ValueError, OSError):
        pass
    return {}


def _ghi_json(du_lieu, duong_dan=DATA_JSON_PATH):
    if file_helper is not None:
        for ten_ham in ("ghi_json", "save_json", "write_json"):
            ham = getattr(file_helper, ten_ham, None)
            if callable(ham):
                try:
                    ham(duong_dan, du_lieu)
                except TypeError:
                    ham(du_lieu, duong_dan)
                return

    with open(duong_dan, "w", encoding="utf-8") as f:
        json.dump(du_lieu, f, ensure_ascii=False, indent=2)


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
    trong `data/data.json` bằng hàm ghi JSON của `file_helper.py`.
    Không ghi đè dữ liệu cũ khi API gặp lỗi hoặc không lấy được dữ liệu.
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

    du_lieu_json = _doc_json(duong_dan_json)
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
    try:
        _ghi_json(du_lieu_json, duong_dan_json)
    except Exception as loi:
        print(f"Lỗi khi ghi file JSON '{duong_dan_json}': {loi}")

    return danh_sach_diem_den


if __name__ == "__main__":
    ket_qua = lay_du_lieu_diem_den("Đà Lạt", limit=3)
    for dd in ket_qua:
        print(dd)