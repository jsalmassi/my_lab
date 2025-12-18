from src import main
def test_main_prints(capsys):
    main.main()
    captured = capsys.readouterr()
    assert "Hello from my_lab" in captured.out
# --- IGNORE ---