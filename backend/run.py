from app import create_app
import os
# from app.services.report_service.scheduler import schedule_jobs
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = create_app()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()  # optional if not already loaded in create_app()
    # schedule_jobs(app)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
    