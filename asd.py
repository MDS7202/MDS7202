mascotas_df["descripción"].apply(lambda x: strip_accents_ascii(x)).str.replace(
    "\(|\)|,|\d{1,3}|;|\.", " ", regex=True
).replace(r"\s+", " ", regex=True).str.strip().str.lower()
