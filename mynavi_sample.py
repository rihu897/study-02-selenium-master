import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import logging

### Chromeを起動する関数
def set_driver(driver_path,headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg==True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    #options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "\\" + driver_path,options=options)

### main処理
def main():
    ### 課題7：処理の経過が分かりやすいようログファイルを出力
    # ログファイル出力
    logging.basicConfig(filename=os.getcwd() + "/debug.log", level=logging.DEBUG)
    # 開始ログ
    logging.info("メイン処理を開始します。")
    ### 課題4：任意のキーワードをコンソール（黒い画面）から指定
    search_keyword=input("検索キーワードを入力してください：")
    # driverを起動
    driver=set_driver("chromedriver.exe",False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(2)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    
    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    
    # データフレーム作成用リスト
    result_list=[[]]

    # ページカウント
    page_count = 1
    # 件数カウント
    count = 1

    ### 課題3：２ページ目以降の情報も含めて取得
    # 次のページがなくなるまでループ
    while True :
        # 開始ログ出力
        logging.info("処理開始：{}ページ目".format(page_count))
        # 会社名、キャッチコピー、雇用形態を取得
        name_list=driver.find_elements_by_class_name("cassetteRecruit__name")
        copy_list=driver.find_elements_by_class_name("cassetteRecruit__copy")
        status_list=driver.find_elements_by_class_name("labelEmploymentStatus")
        # 1ページ分繰り返し
        print("{},{},{}".format(len(copy_list),len(status_list),len(name_list)))
        for name,copy,status in zip(name_list,copy_list,status_list):
            # 開始ログ出力
            logging.info("処理開始：{}件目".format(count))
            ### 課題6：エラー時にスキップして処理を継続させる
            # トランザクション開始
            try :
                print(name.text)
                print(copy.text)
                print(status.text)
                ### 課題5：取得した結果をpandasモジュールを使ってCSVファイルに出力
                # 取得結果をリストに格納
                result_list.append([name.text,copy.text,status.text])
                # 終了ログ出力
                logging.info("正常終了：{}件目".format(count))
            except Exception as e:
                # エラーログ出力
                logging.error("エラーが発生しました：" + str(e))
                # 処理をスキップ
                continue
            finally :
                # 件数を加算
                count += 1
            
        # 終了ログ出力
        logging.info("正常終了：{}ページ目".format(page_count))
        ### 課題3：２ページ目以降の情報も含めて取得
        # トランザクション開始（※次のページの存在確認）
        try :
            # 次のページへのリンク
            next_page = driver.find_element_by_class_name("iconFont--arrowLeft")
            # リンクが画面内に入るまでスクロール（※画面外だとエラーになる）
            driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
            # リンクをクリック
            next_page.click()
            # ページカウントを加算
            page_count += 1
        except :
            # 次のページが存在しない為、ループを終了
            break

    ### 課題5：取得した結果をpandasモジュールを使ってCSVファイルに出力
    # リストの不要部分を削除
    result_list.pop(0)
    # データフレーム作成
    df = pd.DataFrame(result_list, columns=["会社名","キャッチコピー","雇用形態"])
    # 取得結果をCSV出力
    df.to_csv(os.getcwd() + "/result.csv")
    print("結果をCSV出力しました：" + os.getcwd() + ".result.csv")
    
    # 終了ログ
    logging.info("メイン処理を終了します。")

### 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
