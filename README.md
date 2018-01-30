Ĉi tio estas programo por krei kartaron por esperanta versio de
[Codenames](https://boardgamegeek.com/boardgame/178900/codenames).
Ankoraŭ necesas la originala ludo por havi la ceterajn kartojn kiuj
ne temas pri la vortoj.

Se vi volas simple havi la PDF, elŝutu ĝin de [ĉi tie](https://bpeel.github.io/kodvortoj/kodvortoj.pdf).

Alikaze, por ruli la skripton oni unue devas instali la dependajn
pakaĵojn. Ĉe Fedora oni povas ruli la jenan komandon:

    sudo dnf install librsvg2 python3-gobject python3-cairo python3

Poste simple rulu la skripton:

    ./kodvortoj.py

Tio kreos PDF kiu nomiĝas `kodvortoj.pdf`.

Se vi volas aldoni aŭ forigi vortojn vi povas redakti la liston en
`vortoj.txt`.
