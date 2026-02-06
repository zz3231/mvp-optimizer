"""
Test backward compatibility for sensitivity analysis with/without sharpe_impact
"""

import pandas as pd

print("=" * 70)
print("BACKWARD COMPATIBILITY TEST")
print("=" * 70)

# Test 1: Old format data (without sharpe_impact)
print("\n1. Old format data (no sharpe_impact column)")
print("-" * 70)

old_data = pd.DataFrame({
    'asset': ['CA', 'FR', 'CA', 'FR'],
    'direction': ['decrease', 'decrease', 'increase', 'increase'],
    'return_impact': [-0.002, -0.003, 0.002, 0.003],
    'volatility_impact': [0.0, 0.0, 0.0, 0.0]
})

print(f"Columns: {old_data.columns.tolist()}")
has_sharpe = 'sharpe_impact' in old_data.columns
print(f"Has sharpe_impact: {has_sharpe}")

if not has_sharpe:
    print("✓ Detected old format - should show warning and basic view")
    # Try to display old format
    try:
        df_display = old_data[['asset', 'direction', 'return_impact']].copy()
        print(f"✓ Can display: {df_display.columns.tolist()}")
    except KeyError as e:
        print(f"✗ Error: {e}")
else:
    print("✗ Should not have sharpe_impact")

# Test 2: New format data (with sharpe_impact)
print("\n2. New format data (with sharpe_impact column)")
print("-" * 70)

new_data = pd.DataFrame({
    'asset': ['CA', 'FR', 'CA', 'FR'],
    'direction': ['decrease', 'decrease', 'increase', 'increase'],
    'return_impact': [-0.002, -0.003, 0.002, 0.003],
    'volatility_impact': [0.0, 0.0, 0.0, 0.0],
    'sharpe_impact': [-0.016, -0.019, 0.016, 0.019]
})

print(f"Columns: {new_data.columns.tolist()}")
has_sharpe = 'sharpe_impact' in new_data.columns
print(f"Has sharpe_impact: {has_sharpe}")

if has_sharpe:
    print("✓ Detected new format - should show full 4-plot view")
    # Try to display new format
    try:
        df_display = new_data[['asset', 'direction', 'return_impact', 'sharpe_impact']].copy()
        print(f"✓ Can display: {df_display.columns.tolist()}")
    except KeyError as e:
        print(f"✗ Error: {e}")
else:
    print("✗ Should have sharpe_impact")

# Test 3: Simulating app.py logic
print("\n3. Simulating app.py backward compatibility logic")
print("-" * 70)

def test_display_logic(df_return_sens, df_vol_sens):
    """Simulate the app.py display logic"""
    has_sharpe = 'sharpe_impact' in df_return_sens.columns
    
    print(f"has_sharpe: {has_sharpe}")
    
    if not has_sharpe:
        print("  → Show warning: 'Please run sensitivity analysis again'")
        print("  → Display basic view (without sharpe ratio)")
        try:
            # Old format
            df1 = df_return_sens[['asset', 'direction', 'return_impact']].copy()
            df2 = df_vol_sens[['asset', 'direction', 'volatility_impact']].copy()
            print(f"  ✓ Basic view works: {len(df1)} rows")
            return True
        except Exception as e:
            print(f"  ✗ Error in basic view: {e}")
            return False
    else:
        print("  → Display full view (with sharpe ratio + 4 plots)")
        try:
            # New format
            df1 = df_return_sens[['asset', 'direction', 'return_impact', 'sharpe_impact']].copy()
            df2 = df_vol_sens[['asset', 'direction', 'volatility_impact', 'sharpe_impact']].copy()
            print(f"  ✓ Full view works: {len(df1)} rows")
            return True
        except Exception as e:
            print(f"  ✗ Error in full view: {e}")
            return False

print("\nTest with OLD data:")
success1 = test_display_logic(old_data, old_data)

print("\nTest with NEW data:")
success2 = test_display_logic(new_data, new_data)

print("\n" + "=" * 70)
if success1 and success2:
    print("✓ ALL TESTS PASSED")
    print("  - Old data displays basic view")
    print("  - New data displays full view with Sharpe Ratio")
    print("  - No KeyError exceptions")
else:
    print("✗ SOME TESTS FAILED")
print("=" * 70)
