# -*- coding: utf-8 -*-
CURRENT_LANG = "PL"

translations = {}
translations["PL"] = {}
translations["PL"]["view:"] = "Widok:"
translations["PL"]["single"] = "Pojednyczy"
translations["PL"]["vertical"] = "Dwa w pionie"
translations["PL"]["horizontal"] = "Dwa w poziomie"
translations["PL"]["quad"] = "Poczwórny"
translations["PL"]["options"] = "Opcje"
translations["PL"]["Physics simulator"] = "Symulator fizyczny"
translations["PL"]["camera"] = "Kamera"
translations["PL"]["toggle fullscreen"] = "Przełącz tryb pełnoekranowy"
translations["PL"]["option browser:"] = "Panel opcji: "
translations["PL"]["simulation"] = "Symulacja"
translations["PL"]["interactions"] = "Oddziaływania"
translations["PL"]["all_others"] = "Inne"

translations["PL"]["Fullscreen"] = "Pełny ekran"
translations["PL"]["Hide this bar"] = "Ukryj ten panel"
translations["PL"]["show more buttons"] = "Pokaż więcej przycisków"

translations["PL"]["Gravity"] = "Grawitacja"
translations["PL"]["Earth gravity"] = "Grawitacja ziemska"
translations["PL"]["Step size"] = "Rozmiar kroku"
translations["PL"]["is used by buttons << and >>"] = "jest używany przez przyciski << i >>"
translations["PL"]["Backward time direction"] = "Czas do tyłu"
translations["PL"]["Time speed"] = "Tempo"
translations["PL"]["Show grid"] = "Pokaż siatkę"
translations["PL"]["Show axis"] = "Pokaż osie"

translations["PL"]["Prompt on exit"] = "Pytaj przed zamknięciem"
translations["PL"]["Do not use header bar"] = "Nie używaj belki tytułowej"
translations["PL"]["Show tips"] = "Pokazuj podpowiedzi"

translations["PL"]["expected an indented block"] = "Oczekiwano wciętego bloku"
translations["PL"]["unexpected indent"] = "Nieoczekiwane wcięcie"
translations["PL"]["invalid syntax"] = "Nieprawidłowa składnia"
translations["PL"]["name '%s' is not defined"] = "Nazwa '%s' nie została zdefiniowana"
translations["PL"]["'%s' object has no attribute '%s'"] = "Obiekt: '%s' nie posiada atrybutu '%s'"

translations["PL"]["NameError"] = "Błąd nazwy"
translations["PL"]["IndentationError"] = "Błąd wcięcia"
translations["PL"]["SyntaxError"] = "Błąd składni"
translations["PL"]["AttributeError"] = "Błąd atrybutu"

translations["PL"]["left projection"] = "Lewy rzut"
translations["PL"]["right projection"] = "Prawy rzut"
translations["PL"]["top projection"] = "Górny rzut"
translations["PL"]["bottom projection"] = "Dolny rzut"
translations["PL"]["front projection"] = "Przedni rzut"
translations["PL"]["back projection"] = "Tylny rzut"
translations["PL"]["3d view"] = "Widok 3D"

translations["PL"]["Adjust zoom of camera"] = "Dostosuj przybliżenie kamery"
translations["PL"]["zoom in"] = "Przybliż"
translations["PL"]["zoom out"] = "Oddal"

translations["PL"]["Show manipulating options"] = "Pokaż opcje manipulacji kamerą"

translations["PL"]["run simulation"] = "Uruchom symulację"
translations["PL"]["pause simulation"] = "Zatrzymaj symulację"
translations["PL"]["end simulation"] = "Zakończ symulację"
translations["PL"]["step forward"] = "Krok do przodu"
translations["PL"]["step backward"] = "Krok do tyłu"
translations["PL"]["help"] = "Pomoc"

translations["PL"]["The changes will be applied the next time the application restarts"] = "Zmiany zostaną zastosowane po ponownym uruchomieniu aplikacji"
translations["PL"]["Move precisely"] = "Przesuń precyzyjnie"
translations["PL"]["Rotate around axis"] = "Obróć wokół osi"
translations["PL"]["Rotate left"] = "Obróć w lewo"
translations["PL"]["Rotate right"] = "Obróć w prawo"
translations["PL"]["Restart rotation"] = "Zresetuj obrót"
translations["PL"]["Restart position"] = "Zresetuj położenie"

translations["PL"]["Add one ball"] = "Dodaj kulkę"
translations["PL"]["Add many balls"] = "Dodaj kulki"
translations["PL"]["Save as"] = "Zapisz jako"
translations["PL"]["Save"] = "Zapisz"
translations["PL"]["load"] = "Wczytaj"
translations["PL"]["Browse files"] = "Przeglądaj pliki"

translations["PL"]["Please choose a file"] = "Wybierz plik"

translations["PL"]["Overwrite existing file?"] = "Nadpisać istniejący plik?"
translations["PL"]["Do you really want to overwrite existing file?"] = "Czy napewno chcesz nadpisać istniejący plik?"

translations["PL"]["Unsaved changes will be lost.\nPress enter to discard changes and quit immediately."] = "Niezapisane zmiany zostaną utracone.\nNaciśnij enter, aby odrzucić zmiany i zamknąć program."
translations["PL"]["Are you sure you want to quit?"] = "Czy napewno chcesz opuścić program?"

translations["PL"]["gravitation"] = "Grawitacji"

translations["PL"]["To restore option browser use a switcher on a top bar"] = "Aby ponownie otworzyć przeglądarkę opcji, użyj przełącznika ulokowanego na górnym pasku"
translations["PL"]["Press F11 to exit full screen mode."] = "Naciśnij F11, aby opuścić tryb pełnoekranowy."



translations["PL"]["You have too old version of GTK+"] = "Posiadasz zbyt starą wersję GTK+"
translations["PL"]["Do you want to continue?"] = "Kontuunować?"
translations["PL"]["Some functions may not work properly with current GTK+ version."] = "Niektóre funkcje mogą nie działać poprawnie z bieżącą wersją GTK+"
translations["PL"]["You shall upgrade your GTK+ to version 3.12 at least. Your GTK+ version is "] = "Zalecana jest aktualizacja GTK+ do wersji 3.12 lub nowszej. Twoja obecna wersja to "

translations["PL"]["You have an old GTK+ version. If you want to improve an apperance of this application, please upgrade GTK+ to 3.16 version."] = "Posiadasz starą wersję GTK+. Aby poprawić wygląd aplikacji, zaktualizuj proszę GTK+ do wersji 3.16 "





def _(string):

	if string in translations[CURRENT_LANG]:
		return translations[CURRENT_LANG][string]
	else:
		print ("Untranslated string: " + string + " in " + CURRENT_LANG)
		return string
