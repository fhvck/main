# LA BASE
la tua base è quel posto in cui puoi trovare il tuo computer, le cards e il tuo client SMTP.
## il tuo computer
questo è il computer con cui andrai in battaglia. Accedendo a questa schermata puoi leggere un elenco dei tools sbloccati con tanto di documentazione oppure modificare le tue impostazioni

per accedere basta scrivere nel menu principale:
```python
c/ mypc
```
e dalla schermata del tuo computer hai a disposizione questi comandi:
```sh
cd .setts   # per modificare le impostazioni
enable FMTP # abilita il ricevimento delle mail
kill FMTP   # interrompi la ricezione delle mail
help        # mostra la documentazione
```

## comandi
i comandi seguono tutti la STDSYX che sta per Standard Syntax. questa ha come base:
```sh
command -variable value
```
questo eseguirà _command_ dando alla variable _variable_ il valore _value_

esempio pratico
```
select -id 10
```
questo eseguirà il comando select con id=10. questo comando serve per selezionare un nemico sulla mappa usando un suo valore univoco che potrebbe essere il suo id o la posizione, di norma _select_ viene lanciato con id=NULL e pos=NULL e poi automaticamente modificherà la variabile selezionata con il valore specificato. 

prima abbiamo visto che di base abbiamo _command -var val_ per eseguire command con var=val quindi per dire al comando hack di attaccare la porta 80 faremo:

```sh
hack -port 80
```