# -------------------------------------------------
if __name__ == "__main__":
    # FORCE RESET: Safely drop the table and recreate it for the demo
    try:
        conn = get_db()
        conn.execute("DROP TABLE IF EXISTS reports")
        conn.execute("DROP TABLE IF EXISTS feedback_log")
        conn.commit()
        conn.close()
        print("Old database tables dropped.")
    except Exception as e:
        print(f"Could not drop tables: {e}")
        
    init_db()
    print("=" * 50)
    print("Tsebisa Pilot Server starting...")
    print("Citizen reporting:  http://127.0.0.1:5000/")
    print("Partner dashboard:  http://127.0.0.1:5000/dashboard")
    print("User guide:         http://127.0.0.1:5000/guide")
    print("=" * 50)
    
    # Required for Render deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)