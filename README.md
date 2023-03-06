# _Sparx EA Diagram Generator v.1.0.beta_
### _by KoTA 308_

Sparx EA Diagram Generator merupakan sebuah tools yang pembuatan diagram Use Case untuk Sparx EA dari file CSV to XML.

Prerequisted
- clone repositories
- python
- Sparx EA
- VSCode

## How to Run Project
berikut langkah langkah untuk menguji prototype v.1.0.beta
- Buka integrated terminal pada VSCode
- Change directory menuju folder prototype
```cd Prototype```
- Jalankan file ```use_generator_py.py``` dengan memnggunakan python
    ```
    python3 use_case_generator.py
    ```
    atau
    ```
    python use_case_generator.py
    ```
- Inputkan ```CSV-ok.csv``` untuk menjadi input, jika Anda mempunyai file csv lainnya untuk dicoba masukkan nama file yang ingin dicoba
- Pastikan path dan nama file benar, jika sudah selesai hasil generate akan dituliskanpada ```output.xml```
- File XML siap diimport ke Sparx EA

## How to Import
- Buka project atau buat project baru unutk mengimport file XML.
- Tekan tab "Publish" > "Import XML" > "Import Package from XMI"
- Pilih file yang tadi telah digenerate, lalu tekan tombol "Import"
- Tunggu sampai proses berhasil
- Package yang berisi Use Case Diagram telah berhasil diimport

Mengalami error? contact *Marissa Nur Amalia*