from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rejestracja", methods=['POST', 'GET'])
def rejestracja():
    return render_template("rejestracja.html")

@app.route("/rejestracja-zapisz", methods=['POST', 'GET'])
def rejestracjazapis():
  db = sqlite3.connect("data.db")
  cursor = db.cursor()
  idkierowcy= request.form.get('idkierowcy')
  haslo= request.form.get('password')
  mail= request.form.get('email')
  cursor.execute(f"SELECT idkierowcy FROM kierowcy")
  wynik = cursor.fetchall()
  cursor.execute("INSERT INTO kierowcy(idkierowcy, haslo) VALUES(?, ?)", (str(idkierowcy), str(haslo)))
  db1 = sqlite3.connect("users.db")
  cursor1 = db1.cursor()
  cursor1.execute(f"CREATE TABLE IF NOT EXISTS {idkierowcy}(tor STR, najlepszy_czas STR, okrazenia INT, data STR)")
  db1.commit()
  db.commit()
  db1.close()
  db.close()
  return redirect("/rejestracja")

@app.route("/zarejestruj-przejazd")
def odwiedziny():
    return render_template("tory.html")

@app.route("/nowy-tor")
def nowytor():
    return render_template("zglostor.html")

@app.route("/zapisz-tor", methods=['POST', 'GET'])
def zapisztor():
  db = sqlite3.connect("nowytor.db")
  cursor = db.cursor()
  adres= request.form.get('adrest')
  nazwa= request.form.get('nazwat')
  wojewodztwo= request.form.get('wojt')
  cursor.execute(f"SELECT * FROM nowytor")
  cursor.execute("INSERT INTO nowytor(nazwa, adres, województwo) VALUES(?, ?, ?)", (str(nazwa), str(adres), str(wojewodztwo)))
  db.commit()
  db.close()
  return redirect("/nowy-tor")

@app.route("/szukaj-kierowcy")
def kierowcy():
    return render_template("kierowcy.html")

@app.route("/zapisz-przejazd", methods=['POST', 'GET'])
def zapisz():
  db = sqlite3.connect("data.db")
  db1 = sqlite3.connect("users.db")
  cursor1 = db1.cursor()
  cursor = db.cursor()
  tor = request.form.get('tor')
  czas= request.form.get('besttime')
  okrazenia= request.form.get('laps')
  idkierowcy= request.form.get('idkierowcy')
  haslo = request.form.get('haslo')
  data = request.form.get('data')
  cursor.execute(f"SELECT haslo FROM kierowcy WHERE idkierowcy LIKE '{idkierowcy}'")
  wynik = cursor.fetchall()
  print(wynik)
  x = str((wynik[0][0]))
  if x == haslo:
    cursor1.execute(f"INSERT INTO {idkierowcy}(tor, najlepszy_czas, okrazenia, data) VALUES(?, ?, ?, ?)", (str(tor), str(czas), int(okrazenia), str(data)))
  else:
    return("niepoprawne hasło dla tego loginu!")
  db.commit()
  db.close()
  db1.commit()
  db1.close()
  return redirect("/zarejestruj-przejazd")
@app.route("/szukaj-kierowcy/<idkierowcy>", methods=['POST', 'GET'])
def szukajkiero(idkierowcy):
  db = sqlite3.connect("users.db")
  cursor = db.cursor()
  cursor.execute(f"SELECT * FROM {idkierowcy}")
  wynik = cursor.fetchall()
  return render_template("panel_kierowcy.html", wynik=wynik, len = len(wynik))

@app.route("/szukaj-kierowcy/szukaj", methods=['POST', 'GET'])
def szukajkierowcy():
  idkierowcy= request.form.get('idkierowcy')
  return redirect(f"/szukaj-kierowcy/{idkierowcy}")
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'),500

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'),404


if __name__ == "__main__":
    app.run(debug=False)