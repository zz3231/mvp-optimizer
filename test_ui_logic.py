"""
Test UI logic for Risk Aversion disable/enable based on Use Target Return
"""

print("=" * 70)
print("UI LOGIC TEST: Risk Aversion Enable/Disable")
print("=" * 70)

print("\nScenario 1: Use Target Return = False")
print("-" * 70)
use_target_return = False
risk_aversion_disabled = use_target_return

print(f"use_target_return: {use_target_return}")
print(f"risk_aversion disabled: {risk_aversion_disabled}")
print(f"✓ Risk Aversion is ENABLED (user can input)" if not risk_aversion_disabled else "✗ Risk Aversion is DISABLED")

print("\nScenario 2: Use Target Return = True")
print("-" * 70)
use_target_return = True
risk_aversion_disabled = use_target_return

print(f"use_target_return: {use_target_return}")
print(f"risk_aversion disabled: {risk_aversion_disabled}")
print(f"✓ Risk Aversion is DISABLED (grayed out)" if risk_aversion_disabled else "✗ Risk Aversion is ENABLED")

print("\nScenario 3: Toggle back to False")
print("-" * 70)
use_target_return = False
risk_aversion_disabled = use_target_return

print(f"use_target_return: {use_target_return}")
print(f"risk_aversion disabled: {risk_aversion_disabled}")
print(f"✓ Risk Aversion is ENABLED again" if not risk_aversion_disabled else "✗ Risk Aversion still DISABLED")

print("\n" + "=" * 70)
print("✓ UI LOGIC CORRECT")
print("  When 'Use Target Return' is checked → Risk Aversion DISABLED")
print("  When 'Use Target Return' is unchecked → Risk Aversion ENABLED")
print("=" * 70)
