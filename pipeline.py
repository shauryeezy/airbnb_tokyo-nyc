import load_data
import transform_data
import export_analytics
import sys

def main():
    """
    Master Orchestration Script.
    Executes the full ELT pipeline: Extract/Load -> Transform -> Export.
    """
    print("==================================================")
    print("🌎 GLOBAL PROPERTY MARKET ANALYTICS PIPELINE")
    print("==================================================")

    # Step 1: Ingestion
    print("\n[PHASE 1] DATA INGESTION (EL)")
    try:
        load_data.load_data()
    except Exception as e:
        print(f"❌ Pipeline Failed at Ingestion: {e}")
        sys.exit(1)

    # Step 2: Transformation
    print("\n[PHASE 2] DATA TRANSFORMATION & ANALYTICS")
    try:
        transform_data.transform()
    except Exception as e:
        print(f"❌ Pipeline Failed at Transformation: {e}")
        sys.exit(1)
        
    # Step 3: Export
    print("\n[PHASE 3] REPORT GENERATION")
    try:
        export_analytics.export_valuation_model()
    except Exception as e:
        print(f"❌ Pipeline Failed at Export: {e}")
        sys.exit(1)

    print("\n==================================================")
    print("✅ PIPELINE EXECUTION SUCCESSFUL")
    print("==================================================")

if __name__ == "__main__":
    main()
