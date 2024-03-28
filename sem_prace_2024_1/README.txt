Podrobnosti o implementac:
- Používá bitové operace k úpravě nejméně významných bitů dat pixelů v obrázku BMP.
- Zachová hlavičku BMP (54 bajtů pro nekomprimované obrázky) během procesu steganografie.
- Funkce `hide` přečte steganografický obraz a vstupní soubor, provede LSB steganografii a uloží upravený obraz do skrytého souboru.
- Funkce `decode` přečte upravený obrázek BMP, extrahuje skryté bajty souborů z nejméně významných bitů dat pixelů a uloží extrahovaný soubor.

Omezení:
- Předpokládá, že obrázek steganografie je nekomprimovaný soubor BMP.
- Nezahrnuje zpracování chyb nebo bezpečnostní opatření.
- Nelze skrýt soubory větší než dostupné místo na obrázku steganografie.