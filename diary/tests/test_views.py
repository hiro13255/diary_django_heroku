from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import Diary

class LoggedInTestCase(TestCase):
    '''各テストクラスで共通の事前準備処理をオーバーライドしたTestCaseクラス'''

    def setUp(self):
        '''テストメソッド実行前の事前設定'''

        #テストユーザーのパスワード
        self.password = '<パスワード>'

        #各インスタンスメソッドで使うテスト用ユーザを生成
        #インスタンス変数に格納
        self.test_user = get_user_model().objects.create_user(
            username='<ユーザー名>',
            email = '<メールアドレス>',
            password=self.password
        )

        #テストユーザーでログイン
        self.client.login(email=self.test_user.email, password=self.password)

class TestDiaryCreateView(LoggedInTestCase):
    '''DiaryCreateViewのテストクラス'''

    def test_create_diary_success(self):
        '''日記作成ができることを検証'''

        #Postパラメータ
        params = {'title' : 'テストタイトル',
                  'content' : '本文',
                  'photo1' : '',
                  'photo2' : '',
                  'photo3' : ''}

        #新規作成処理（Post）を実行
        respons = self.client.post(reverse_lazy('diary:diary_create'), params)

        #日記リストページへのリダイレクトを検証
        self.assertRedirects(respons,reverse_lazy('diary:diary_list'))

        #日記データがDBに登録されたか検証
        self.assertEqual(Diary.objects.filter(title='テストタイトル').count(),1)

    def test_create_diary_failure(self):
        '''新規作成失敗を検証'''

        #新規日記作成処理を実行
        respons = self.client.post(reverse_lazy('diary:diary_create'))

        #必須フォームを入力していないのでエラーになることを検証
        self.assertFormError(respons, 'form', 'title', 'このフィールドは必須です。')

class TestDiaryUpdateView(LoggedInTestCase):
    '''DiaryUpdateViewのテストクラス'''

    #編集処理が成功することを検証
    def test_update_success(self):
        #テスト用の日記データ作成
        diary = Diary.objects.create(user=self.test_user, title='タイトル編集前')

        #Postパラメータ
        params = {'title': 'タイトル編集後'}

        # 日記編集処理(Post)を実行
        response = self.client.post(reverse_lazy('diary:diary_update', kwargs={'pk': diary.pk}), params)

        # 日記詳細ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('diary:diary_detail', kwargs={'pk': diary.pk}))

        # 日記データが編集されたかを検証
        self.assertEqual(Diary.objects.get(pk=diary.pk).title, 'タイトル編集後')

    #編集処理が失敗することを検証
    def test_update_diary_dailure(self):
        #編集処理実行（Post)
        respons = self.client.post(reverse_lazy('diary:diary_update', kwargs={'pk': 999}))

        #存在しない日記データを編集しようとしてエラーになることを検証
        self.assertEqual(respons.status_code, 404)


class TestDiaryDeleteView(LoggedInTestCase):
    '''DiaryDeleteViewのテストクラス'''

    #削除処理が成功することを検証
    def test_delete_diary_success(self):
        #テスト用の日記データ作成
        diary = Diary.objects.create(user=self.test_user, title='タイトル')

        #削除処理実行（Post）
        respons = self.client.post(reverse_lazy('diary:diary_delete', kwargs={'pk': diary.pk}))

        #日記リストページへリダイレクトを検証
        self.assertRedirects(respons, reverse_lazy('diary:diary_list'))

        #日記データが削除されたか検証
        self.assertEqual(Diary.objects.filter(pk=diary.pk).count(),0)

    #削除処理が失敗することを検証
    def test_delete_diary_failure(self):
        #削除処理実行（Post）
        respons = self.client.post(reverse_lazy('diary:diary_delete', kwargs={'pk': 999}))

        #存在しない日記データを削除しようとしてエラーになることを検証
        self.assertEqual(respons.status_code,404)
