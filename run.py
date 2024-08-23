from app import create_app
import webview
import logging

if __name__ == '__main__':
    app = create_app()
    try:
        webview.create_window("Tavella's - Pedal Pulse", app)
        webview.start()
    except Exception as e:
        logging.error("Ocorreu um erro ao iniciar o webview:", exc_info=True)
    # app.run(host="0.0.0.0", port=5050)