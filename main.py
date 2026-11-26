
# Quiz Game

import json
import random
from datetime import datetime
from pathlib import Path


# 숫자 입력 검증 함수
def get_valid_number(prompt, min_value, max_value):
    while True:
        value = input(prompt).strip()

        # 빈 입력(그냥 Enter)은 따로 안내 후 다시 입력받기
        if not value:
            print("입력값이 비어 있습니다. 숫자를 입력하세요.")
            continue

        try:
            value = int(value)

            if min_value <= value <= max_value:
                return value
            else:
                print(f"{min_value}~{max_value} 사이의 숫자를 입력하세요.")

        except ValueError:
            print("숫자만 입력할 수 있습니다.")


# 빈 문자열 입력 검증 함수
def get_valid_text(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("내용을 입력해야 합니다.")


# Quiz class
class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def show_hint(self):
        if self.hint:
            print(f"힌트: {self.hint}")
        else:
            print("이 퀴즈에는 힌트가 없습니다.")

    def display(self):
        print(self.question)

        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def check_answer(self, user_answer):
        return self.answer == user_answer


# QuizGame class
class QuizGame:
    def __init__(self):
        self.state_file = Path(__file__).with_name("state.json")
        self.best_score = 0
        self.best_question_count = 0
        self.history = []

        self.quizzes = self.get_default_quizzes()

        self.load_state()

    # 점수 계산
    def calculate_score(self, correct_count, total_count):
        if total_count == 0:
            return 0

        return int(correct_count / total_count * 100 + 0.5)

    # JSON 파일 저장
    def save_state(self, show_message=True):
        data = {
            "best_score": self.best_score,
            "best_question_count": self.best_question_count,
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                    "hint": quiz.hint
                }
                for quiz in self.quizzes
            ],
            "history": self.history
        }

        try:
            with self.state_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            if show_message:
                print("게임 데이터가 저장되었습니다.")

        except OSError as error:
            print(f"데이터 저장 중 오류가 발생했습니다: {error}")

    # JSON 파일 불러오기
    def load_state(self):
        if not self.state_file.exists():
            print("저장된 데이터가 없어 기본 퀴즈를 사용합니다.")
            self.save_state()
            return

        try:
            with self.state_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("저장 데이터 형식이 올바르지 않습니다.")

            best_score = data["best_score"]
            quiz_data = data["quizzes"]

            if type(best_score) is not int or not 0 <= best_score <= 100:
                raise ValueError("최고 점수 데이터가 올바르지 않습니다.")

            best_question_count = data.get("best_question_count", 0)

            if type(best_question_count) is not int or best_question_count < 0:
                raise ValueError("최고 점수 문제 수 데이터가 올바르지 않습니다.")

            if not isinstance(quiz_data, list):
                raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

            history = data.get("history", [])

            if not isinstance(history, list) or not all(
                isinstance(record, dict)
                and isinstance(record.get("date"), str)
                and type(record.get("question_count")) is int
                and type(record.get("correct_count")) is int
                and type(record.get("hint_count")) is int
                and type(record.get("score")) is int
                for record in history
            ):
                raise ValueError("점수 기록 데이터 형식이 올바르지 않습니다.")

            loaded_quizzes = []

            for item in quiz_data:
                question = item["question"]
                choices = item["choices"]
                answer = item["answer"]
                hint = item.get("hint", "")

                if (
                    not isinstance(question, str)
                    or not question.strip()
                    or not isinstance(choices, list)
                    or len(choices) != 4
                    or not all(
                        isinstance(choice, str) and choice.strip()
                        for choice in choices
                    )
                    or type(answer) is not int
                    or not 1 <= answer <= 4
                    or not isinstance(hint, str)
                ):
                    raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")

                loaded_quizzes.append(Quiz(question, choices, answer, hint))

            self.best_score = best_score
            self.best_question_count = best_question_count
            self.quizzes = loaded_quizzes
            self.history = history

            print("저장된 게임 데이터를 불러왔습니다.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError, OSError) as error:
            print(f"저장 데이터에 문제가 있습니다: {error}")
            print("기본 퀴즈 데이터로 복구합니다.")

            self.best_score = 0
            self.best_question_count = 0
            self.quizzes = self.get_default_quizzes()
            self.history = []
            self.save_state()

    # 기본 퀴즈 데이터
    def get_default_quizzes(self):
        return [
            Quiz(
                "조선시대부터 불리던 대전의 옛 이름으로, '큰밭'이라는 순우리말에서 유래한 지명은 무엇인가요?",
                ["누리밭", "한밭", "솔밭", "늘밭"],
                2,
                "대전에 있는 '○○수목원', '○○대학교' 이름에도 쓰여요."
            ),
            Quiz(
                "대한민국 과학기술의 중심지 역할을 하는 대전의 대규모 연구개발 단지의 이름은 무엇인가요?",
                ["대덕연구개발특구", "송도국제연구단지", "오송생명과학단지", "판교테크노밸리"],
                1,
                "대전의 자치구 이름 중 하나가 들어가요."
            ),
            Quiz(
                "1993년에 개최된 대전 엑스포의 공식 마스코트 이름은 무엇인가요?",
                ["반다비", "수호랑", "꿈돌이", "호돌이"],
                3,
                "'미래의 꿈'을 담은 이름이에요."
            ),
            Quiz(
                "대전광역시를 구성하고 있는 자치구의 총 개수는 몇 개일까요?",
                ["3개", "4개", "5개", "6개"],
                3,
                "동구·중구·서구 말고도 2개가 더 있어요."
            ),
            Quiz(
                "대전역 및 중앙로 일원에서 개최되는 대표적인 여름 축제 이름은 무엇인가요?",
                ["대전 한여름 음악제", "대전 0시 축제", "대전 불빛축제", "대전 사이언스 페스티벌"],
                2,
                "하루가 시작되는 시각, 밤 12시와 관련 있어요."
            )
        ]

    # 퀴즈 출제
    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        # 풀 문제 수 선택
        quiz_total = len(self.quizzes)
        question_count = get_valid_number(
            f"몇 문제를 풀까요? (1~{quiz_total}): ", 1, quiz_total
        )

        correct_count = 0
        hint_count = 0

        # 퀴즈 순서를 랜덤하게 섞기
        shuffled_quizzes = random.sample(self.quizzes, question_count)

        for quiz in shuffled_quizzes:
            print()
            quiz.display()
            print()

            hint_used = False

            while True:
                user_answer = get_valid_number(
                    "정답 번호를 입력하세요 (힌트 보기: 0): ", 0, 4
                )

                if user_answer != 0:
                    break

                quiz.show_hint()

                if quiz.hint and not hint_used:
                    hint_used = True
                    hint_count += 1
                    print("힌트를 사용하여 10점이 차감됩니다.")

            if quiz.check_answer(user_answer):
                print("정답입니다!")
                correct_count += 1
            else:
                print("오답입니다.")

        print()

        total_count = question_count
        score = self.calculate_score(correct_count, total_count)

        penalty = hint_count * 10
        score = max(score - penalty, 0)

        print(
            f"이번 점수: {score}점 "
            f"({total_count}문제 중 {correct_count}문제 정답입니다!)"
        )

        if hint_count > 0:
            print(f"힌트 사용: {hint_count}회 (-{penalty}점)")

        # 이번 게임 기록 추가
        self.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "question_count": total_count,
            "correct_count": correct_count,
            "hint_count": hint_count,
            "score": score
        })

        # 최고 점수 갱신: 전체 문제를 푼 판만 인정, 동점이면 더 많이 푼 기록 우선
        if question_count < quiz_total:
            print(f"※ 전체 문제({quiz_total}문제)를 풀어야 최고 점수에 반영됩니다.")

        elif score > self.best_score or (
            score == self.best_score
            and question_count > self.best_question_count
        ):
            self.best_score = score
            self.best_question_count = question_count
            print("축하합니다! 최고 점수가 갱신되었습니다!")

        self.save_state(show_message=False)
        print("이번 게임 기록이 저장되었습니다.")

    # 퀴즈 추가
    def add_quiz(self):
        question = get_valid_text("새로운 퀴즈 질문을 입력하세요 (취소: 0): ")

        if question == "0":
            print("퀴즈 추가를 취소했습니다.")
            return

        choices = []

        for i in range(1, 5):
            choice = get_valid_text(f"{i}번 보기 입력: ")
            choices.append(choice)

        answer = get_valid_number(
            "정답 번호를 입력하세요 (1~4): ", 1, 4
        )

        hint = input("힌트를 입력하세요 (없으면 Enter): ").strip()

        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)

        self.save_state(show_message=False)
        print("\n새로운 퀴즈가 추가되어 저장되었습니다!")

    # 퀴즈 목록
    def show_quizzes(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해 주세요.")
            return

        print("\n===== 퀴즈 목록 =====")

        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"{i}. {quiz.question}")

        print(f"\n총 {len(self.quizzes)}개의 퀴즈가 있습니다.")

    # 퀴즈 삭제
    def delete_quiz(self):
        if not self.quizzes:
            print("\n삭제할 퀴즈가 없습니다.")
            return

        self.show_quizzes()

        quiz_number = get_valid_number(
            f"\n삭제할 퀴즈 번호를 입력하세요 (1~{len(self.quizzes)}, 취소: 0): ",
            0, len(self.quizzes)
        )

        if quiz_number == 0:
            print("삭제를 취소했습니다.")
            return

        deleted_quiz = self.quizzes.pop(quiz_number - 1)

        print(f"\n{quiz_number}번 퀴즈가 삭제되었습니다.")
        print(f"삭제된 퀴즈: {deleted_quiz.question}")
        self.save_state()

    # 최고 점수 및 점수 기록 확인
    def show_scores(self):
        if self.best_question_count > 0:
            print(
                f"\n현재 최고 점수: {self.best_score}점 "
                f"({self.best_question_count}문제)"
            )
        else:
            print(f"\n현재 최고 점수: {self.best_score}점")

        print("\n===== 점수 기록 =====")

        if not self.history:
            print("아직 게임 기록이 없습니다.")
            return

        for i, record in enumerate(self.history, start=1):
            print(
                f"{i}. {record['date']} | "
                f"{record['question_count']}문제 중 {record['correct_count']}문제 정답 | "
                f"힌트 {record['hint_count']}회 | {record['score']}점"
            )

        print(f"\n총 {len(self.history)}개의 기록이 있습니다.")

    # 메인 메뉴
    def run(self):
        try:
            while True:
                print("\n===== 파이썬 퀴즈 게임 =====")
                print()
                print("1. 퀴즈 풀기")
                print("2. 퀴즈 추가")
                print("3. 퀴즈 목록 보기")
                print("4. 점수 확인 (최고 점수·기록)")
                print("5. 퀴즈 삭제")
                print("6. 종료")
                print()
                print("※ Ctrl+C를 누르면 프로그램을 종료할 수 있습니다.")
                print()

                choice = get_valid_number(
                    "원하는 메뉴 번호를 선택하세요: ", 1, 6
                )

                if choice == 6:
                    print("프로그램을 종료합니다.")
                    break

                elif choice == 1:
                    self.play()

                elif choice == 2:
                    self.add_quiz()

                elif choice == 3:
                    self.show_quizzes()

                elif choice == 4:
                    self.show_scores()

                elif choice == 5:
                    self.delete_quiz()

        except KeyboardInterrupt:
            print("\n사용자 요청으로 프로그램을 종료합니다.")

        except EOFError:
            print("\n입력이 종료되어 프로그램을 종료합니다.")

        # 정상 종료, Ctrl+C, 입력 종료 중 어떤 경우든 마지막에 한 번 저장
        finally:
            self.save_state()


# 게임 실행
if __name__ == "__main__":
    game = QuizGame()
    game.run()
