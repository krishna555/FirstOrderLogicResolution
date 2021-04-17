Husband(Sita, Julius).
Sister(Mary, Sita).
Sister(x, y) => Sister(y, x).
Sister(x, y) & Queen(x) => Queen(y).
Queen(Mary).
Husband(Mary, John).
King(x) :- Husband(y, x),Queen(y).
Beautiful(x) :- Queen(x).
