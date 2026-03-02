import re
text = open("Practice5/raw.txt", encoding="utf-8").read()
Money = r"\d[\d ]*,\d{2}"
to_float = lambda s: float(s.replace(" ", "").replace(",", "."))
datetime = re.search(r"\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2}", text)
pay = re.search(r"Банковская карта|Наличные", text, re.I)
items = []
pattern = rf"(?ms)^\d+\.\n(.*?)\n\d+,\d{{3}} x {Money}\n({Money})"
for m in re.finditer(pattern, text):
    items.append({"название": m.group(1), "цена": to_float(m.group(2))})
sum_items = sum(n["цена"] for n in items)

print("Дата/время:", datetime.group(0))
print("Способ оплаты:", pay.group(0))
print("Количество товаров:", len(items))
print("Итоговая сумма:", sum_items)
print("\nТовары:")
i = 1
for it in items:
    print(f"{i}) {it['название']} — {it['цена']}")
    i +=1

