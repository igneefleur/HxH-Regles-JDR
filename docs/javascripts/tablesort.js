// Active le tri par colonne sur tous les tableaux de contenu,
// à la manière des tables de référence de 5e.tools.
document$.subscribe(function () {
  var tables = document.querySelectorAll("article table:not([class])")
  tables.forEach(function (table) {
    new Tablesort(table)
  })
})
