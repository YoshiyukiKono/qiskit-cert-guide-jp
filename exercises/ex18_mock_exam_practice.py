# exercises/ex18_mock_exam_practice.py
"""
Exercise 18: mock exam practice

学習目標:
- 回路出力予測
- ゲート恒等式
- Sampler / Estimator の使い分け
"""

QUESTIONS = [
    {
        "question": "Hを2回かけると何になるか？",
        "answer": "I",
        "explanation": "H^2 = I。元の状態に戻る。",
    },
    {
        "question": "HZH は何と等価か？",
        "answer": "X",
        "explanation": "Hadamardで基底変換するとZはXとして働く。",
    },
    {
        "question": "Bell状態 (|00> + |11>) / sqrt(2) の測定結果は？",
        "answer": "00 and 11",
        "explanation": "01と10は出ない。完全相関を持つ。",
    },
    {
        "question": "Samplerが返すものは？",
        "answer": "sampled distribution",
        "explanation": "Samplerは測定結果の分布を返す。",
    },
    {
        "question": "Estimatorが返すものは？",
        "answer": "expectation value",
        "explanation": "Estimatorはobservableの期待値を返す。",
    },
]

for i, item in enumerate(QUESTIONS, start=1):
    print(f"\nQ{i}. {item['question']}")
    print(f"Answer: {item['answer']}")
    print(f"Explanation: {item['explanation']}")
