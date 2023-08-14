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
    Or(AKnight, AKnave),  # A is either a Knight or a Knave
    Not(And(AKnight, AKnave)),  # A isn't both a Knight and a Knave
    Implication(AKnight, Not(And(AKnight, AKnave))),  # If A is a Knight, then A isn't both Knight and Knave
    Implication(AKnave, And(AKnight, AKnave))  # If A is a Knave (and thus lying), then A is saying he's both, which is a lie
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),  # A is either a Knight or a Knave
    Not(And(AKnight, AKnave)),  # A cannot be both a Knight and a Knave
    
    Or(BKnight, BKnave),  # B is either a Knight or a Knave
    Not(And(BKnight, BKnave)),  # B cannot be both a Knight and a Knave
    
    Implication(AKnight, And(AKnave, BKnave)),  # If A is a Knight, both A and B are Knaves
    Implication(AKnave, Or(AKnight, BKnight))   # If A is a Knave, at least one of A or B is a Knight
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),  # A is either a Knight or a Knave
    Not(And(AKnight, AKnave)),  # A cannot be both a Knight and a Knave
    
    Or(BKnight, BKnave),  # B is either a Knight or a Knave
    Not(And(BKnight, BKnave)),  # B cannot be both a Knight and a Knave
    
    # A's Statements
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    
    # B's Statements
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Basic Assumptions about A, B, and C
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    
    # B's statements
    Implication(BKnight, And(AKnight, AKnave)),
    Implication(BKnave, Or(AKnight, AKnave)),
    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),
    
    # C's statement
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave)
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
