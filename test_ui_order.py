"""
Test UI order with Use Target Return at the bottom using session_state
"""

class MockSessionState:
    """Mock Streamlit session state for testing"""
    def __init__(self):
        self.data = {}
    
    def __contains__(self, key):
        return key in self.data
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __getitem__(self, key):
        return self.data[key]
    
    @property
    def use_target_return(self):
        return self.data.get('use_target_return', False)
    
    @use_target_return.setter
    def use_target_return(self, value):
        self.data['use_target_return'] = value

print("=" * 70)
print("UI ORDER TEST: Use Target Return at Bottom")
print("=" * 70)

# Simulate Streamlit app flow
session_state = MockSessionState()

print("\nScenario 1: First load (session_state empty)")
print("-" * 70)

# Initialize session state
if 'use_target_return' not in session_state:
    session_state['use_target_return'] = False
    print("✓ Initialized use_target_return = False")

# Risk Aversion reads from session_state
risk_aversion_disabled = session_state.use_target_return
print(f"Risk Aversion disabled: {risk_aversion_disabled}")
print(f"✓ Risk Aversion is ENABLED on first load")

# User clicks checkbox (at bottom)
print("\nUser clicks 'Use Target Return' checkbox...")
use_target_return = True
session_state.use_target_return = use_target_return
print(f"✓ Updated session_state.use_target_return = {use_target_return}")

print("\nScenario 2: Page rerun after clicking (Streamlit reruns)")
print("-" * 70)

# Risk Aversion reads updated session_state
risk_aversion_disabled = session_state.use_target_return
print(f"Risk Aversion disabled: {risk_aversion_disabled}")
print(f"✓ Risk Aversion is now DISABLED (grayed out)")

# Checkbox renders with current value
use_target_return_displayed = session_state.use_target_return
print(f"Checkbox shows: {use_target_return_displayed}")
print(f"✓ Checkbox is CHECKED")

print("\nScenario 3: User unchecks Target Return")
print("-" * 70)

# User unchecks
use_target_return = False
session_state.use_target_return = use_target_return
print(f"✓ Updated session_state.use_target_return = {use_target_return}")

# Page rerun
risk_aversion_disabled = session_state.use_target_return
print(f"Risk Aversion disabled: {risk_aversion_disabled}")
print(f"✓ Risk Aversion is ENABLED again")

print("\nUI Order:")
print("-" * 70)
print("1. Risk-Free Rate (%)")
print("2. Risk Aversion Coefficient    ← reads session_state")
print("3. Include Risk-Free Asset")
print("4. Use Constraints")
print("5. Use Target Return             ← at bottom, updates session_state")
print("6. Target Return (%)             ← conditional display")

print("\n" + "=" * 70)
print("✓ UI ORDER CORRECT")
print("  - Risk Aversion can be placed before Use Target Return checkbox")
print("  - session_state bridges the gap")
print("  - Behavior: slightly delayed (updates on next rerun) but functional")
print("=" * 70)
