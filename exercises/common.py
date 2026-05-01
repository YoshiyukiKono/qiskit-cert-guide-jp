# exercises/common.py
"""
Qiskit資格対策 演習共通ユーティリティ

目的:
- Statevectorを読みやすく表示する
- 確率分布を表示する
- 各演習ファイルから再利用する

前提:
pip install qiskit qiskit-aer matplotlib
"""

from qiskit.quantum_info import Statevector


def show_state(qc):
    """測定前の量子状態を Statevector として表示する。"""
    state = Statevector.from_instruction(qc)
    print(state)
    print(state.to_dict())
    return state


def show_probabilities(qc):
    """測定確率を辞書形式で表示する。"""
    state = Statevector.from_instruction(qc)
    probs = state.probabilities_dict()
    print(probs)
    return probs
