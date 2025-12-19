# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 20:54:22 2025

@author: waiam
"""
import random

def distribute_cards(players, used_cards=None):
    """
    プレイヤー数に応じてカードをシャッフルし、それぞれに配る。
    各プレイヤーは自分のカードを見ずに、他プレイヤーのカードのみを確認。
    """
    # コヨーテのカード構成（合計36枚）
    all_cards = (
        [1] * 4 + [2] * 4 + [3] * 4 + [4] * 4 + [5] * 4 + 
        [10] * 3 + [15] * 2 + [20] * 1 + [0] * 3 + [-5] * 2 + [-10] * 1 + 
        ["×2"] * 1 + ["MAX→0"] * 1 + ["？"] * 1 + ["0（夜）"] * 1
    )
    
    # 使用したカードを正しく除外（夜カードが使われた場合はリセット）
    if used_cards is None or "0（夜）" in used_cards:
        remaining_cards = list(all_cards)
    else:
        remaining_cards = list(all_cards)  # 元のカードプールをコピー
        for card in used_cards:
            if card in remaining_cards:
                remaining_cards.remove(card)  # 1枚ずつ正しく取り除く
    
    # カードをシャッフル
    print(remaining_cards)
    random.shuffle(remaining_cards)
    
    # 各プレイヤーに1枚ずつ配る
    player_cards = {players[i]: remaining_cards[i] for i in range(len(players))}
    
    # 各プレイヤーが見える情報を作成
    player_views = {}
    for i in range(len(players)):
        player_name = players[i]
        visible_cards = [player_cards[players[j]] for j in range(len(players)) if j != i]
        player_views[player_name] = visible_cards
    
    return player_cards, player_views, list(player_cards.values())

def reveal_mystery_card(used_cards):
    """
    「？」カードの正体を未使用のカードの中からランダムに決める
    """
    possible_values = [1, 2, 3, 4, 5, 10, 15, 20, 0, -5, -10]  # 数値カードのみ対象
    remaining_choices = [card for card in possible_values if card not in used_cards]
    return random.choice(remaining_choices) if remaining_choices else 0

def calculate_total(player_cards, used_cards):
    """
    プレイヤーのカードの合計値を算出
    """
    total = sum(value for value in player_cards.values() if isinstance(value, int))
    
    # 「？」カードの処理（コヨーテが宣言されたときに決まる）
    if "？" in player_cards.values():
        mystery_card_value = reveal_mystery_card(used_cards)
        total += mystery_card_value
        print(f"『？』カードの正体は {mystery_card_value} でした！")
    
    # MAX→0 の処理（最大の数値カードを0にする、0（夜）は数値0として扱う）
    if "MAX→0" in player_cards.values():
        num_cards = [value if isinstance(value, int) else 0 for value in player_cards.values()]
        
        # 数値カードが1枚以上ある場合のみ MAX→0 を適用
        if any(isinstance(value, int) for value in player_cards.values()):
            max_value = max(num_cards)
            print(f"MAX→0適用前: {num_cards}, 最大値: {max_value}")
            total -= max_value
            print(f"MAX→0適用後の合計値: {total}")
        else:
            print("MAX→0 の効果を適用しません（数値カードが存在しないため）")
    
    # ×2 の処理（合計値が0以上の場合のみ適用）
    if "×2" in player_cards.values() and total > 0:
        total *= 2
        print("×2 の効果で合計値が倍になりました！")
    
    return total

def check_coyote(final_call, total_value):
    """
    コヨーテの成否判定
    """
    return final_call > total_value

# 例: 4人プレイ
players = ["霊夢", "魔理沙","妖夢","咲夜"]
lives = {
    "霊夢": 2,
    "魔理沙": 3,
    "妖夢": 3,
    "咲夜": 2
}# 各プレイヤーのライフを3に設定
used_cards = []

while len(players) > 1:
    player_cards, player_views, round_used_cards = distribute_cards(players, used_cards)
    used_cards.extend(round_used_cards)
    
    # 各プレイヤーの見えているカードを表示
    for player, visible_cards in player_views.items():
        print(f"{player}が見えているカード: {visible_cards}")
    
    # コールの入力（最終コール）
    final_call = int(input("最終コールの値を入力してください: "))
    
    total_value = calculate_total(player_cards, used_cards)
    
    
    # コヨーテの判定
    challenger = input("コヨーテを宣言したプレイヤーを入力してください: ")
    print(f"実際の合計値は {total_value} です。")
    if check_coyote(final_call, total_value):
        print("コヨーテ成功！最終コールは実際の合計値を超えていました。")
        failed_player = input("ライフを失うプレイヤーを入力してください: ")
    else:
        print("コヨーテ失敗！最終コールは実際の合計値以内でした。")
        failed_player = challenger  # 失敗時はコヨーテしたプレイヤーがライフを失う
    
    if failed_player in lives:
        lives[failed_player] -= 1
        print(f"{failed_player} のライフは残り {lives[failed_player]} です。")
        if lives[failed_player] <= 0:
            print(f"{failed_player} は脱落しました！")
            players.remove(failed_player)
            del lives[failed_player]
    
    # 夜カードの処理（夜カードが出たらカードリセット）
    if "0（夜）" in round_used_cards:
        print("夜カードが出たため、全カードをリセットします。")
        used_cards = []
    
    # 次のラウンドを続けるか確認
    cont = input("次のラウンドを開始しますか？ (y/n): ")
    if cont.lower() != 'y':
        break

# 最後のプレイヤーが勝利
if len(players) == 1:
    print(f"{players[0]} の勝利です！")