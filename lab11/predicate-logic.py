import pytholog as pl

# Every child loves Santa.
# ∀ x (CHILD(x) → LOVES(x,Santa))

# Everyone who loves Santa loves any reindeer.
# ∀ x (LOVES(x,Santa) → ∀ y (REINDEER(y) → LOVES(x,y)))

# Rudolph is a reindeer, and Rudolph has a red nose.
# REINDEER(Rudolph) ∧ REDNOSE(Rudolph)

# Anything which has a red nose is weird or is a clown.
# ∀ x (REDNOSE(x) → WEIRD(x) ∨ CLOWN(x))

# No reindeer is a clown.
# ∀ x (REINDEER(x) → ¬ CLOWN(x))

# Scrooge does not love anything which is weird.
# ∀ x (WEIRD(x) → ¬ LOVES(Scrooge,x))

# (Conclusion) Scrooge is not a child.
# ¬ CHILD(Scrooge)

facts_kb = pl.KnowledgeBase('facts')
facts_kb([
    "loves(X, santa) :- child(X)",
    "loves(X, Y) :- loves(X, santa), reindeer(Y)",
    "reindeer(rudolph)",
    "has_red_nose(rudolph)",
    "weird(X) :- has_red_nose(X)",
    "clown(X) :- has_red_nose(X)",
    "not(clown(X)) :- reindeer(X)",
    "not(loves(scrooge, X)) :- weird(X)",
])

ans = facts_kb.query(pl.Expr("not(child(scrooge))"))
print("Scrooge is child:", *ans)
