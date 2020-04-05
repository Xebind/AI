from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
            Biconditional(AKnight, And(AKnight, AKnave)),
            Biconditional(AKnave, Not(And(AKnight, AKnave))),
            Not(BKnight),
            Not(BKnave),
            Not(CKnight),
            Not(CKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
            Biconditional(AKnight, And(AKnave, BKnave)),
            Biconditional(AKnave, Not(And(AKnave, BKnave))),
            Or(BKnight, BKnave),
            #Biconditional(BKnight, ),
            #Biconditional(BKnave, ),
            Not(CKnight),
            Not(CKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
        Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
        Biconditional(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
        Biconditional(BKnight, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
        Biconditional(BKnave, Not(Not(Or(And(AKnight, BKnight), And(AKnave, BKnave))))),
        Not(CKnight),
        Not(CKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
            Biconditional(AKnight, Or(AKnight, AKnave)),
            Biconditional(AKnave, Not(Or(AKnight, AKnave))),
            Biconditional(BKnight, And(AKnave, CKnave)),
            Biconditional(BKnave, And(AKnight,CKnight)),
            Biconditional(CKnight, AKnight),
            Biconditional(CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
