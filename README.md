# Projenin PyCharmda kurulumu için yapılması gerekenler:
    # virtual env i kur (ubuntu):
    python3.12 -m venv .venv
    source .venv/bin/activate

    # virtual env i kur (windows):
    python3.12 -m venv .venv
    .venv\Scripts\activate


# gerekli dosyaları indir
    pip install -r requirements.txt


# interpreter'ı ayarla:
# Settings > python interpreter > add interpreter > add local interpreter #bu konumdaki ayarları altta belirttiğim gibi ayarla
	environment = existing
	location = .venv/bin/python