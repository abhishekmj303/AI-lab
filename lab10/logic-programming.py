import pytholog as pl

facts_kb = pl.KnowledgeBase('facts')
facts_kb([
    "likes(shyam, mango)",
    "girl(seema)",
    "red(rose)",
    "likes(bill, cindy)",
    "owns(john ,gold)"
])

ans = facts_kb.query(pl.Expr("likes(shyam, What)"))
print(*ans)
