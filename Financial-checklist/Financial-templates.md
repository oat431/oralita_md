# 💰 Financial Tracker — Excel Templates

> **For:** Panomete | **Income:** 32,000 THB/month
> 
> Copy these templates into Excel exactly as written. All formulas are ready to use.

---

## Sheet 1: Daily Expense Tracker

### Column Structure

| Column | Header | Format | Description |
|--------|--------|--------|-------------|
| A | **Date** | Date (YYYY-MM-DD) | Date of expense |
| B | **Category** | Dropdown | Fixed / Variable / Discretionary |
| C | **Description** | Text | What you spent on |
| D | **Amount (THB)** | Number (2 decimal) | How much you spent |
| E | **Running Total** | Formula | Cumulative spending |

### Sample Data

| A (Date) | B (Category) | C (Description) | D (Amount) | E (Running Total) |
|----------|--------------|-----------------|------------|-------------------|
| 2025-01-15 | Fixed | Health Insurance | 4,000.00 | `=SUM(D$2:D2)` |
| 2025-01-15 | Variable | Lunch - Pad Kra Pao | 50.00 | `=SUM(D$2:D3)` |
| 2025-01-15 | Variable | BTS to work | 45.00 | `=SUM(D$2:D4)` |
| 2025-01-15 | Discretionary | Coffee - Starbucks | 180.00 | `=SUM(D$2:D5)` |
| 2025-01-16 | Variable | Dinner - Som Tam | 80.00 | `=SUM(D$2:D6)` |
| 2025-01-16 | Discretionary | Netflix subscription | 349.00 | `=SUM(D$2:D7)` |

### Formulas

```
Cell E2: =SUM(D$2:D2)
Cell E3: =SUM(D$2:D3)
Cell E4: =SUM(D$2:D4)
... (drag down to apply to all rows)

OR use this single formula in E2 and drag down:
=SUM(D$2:D2)
```

### Dropdown Setup (Data Validation)

For Column B (Category):
1. Select all cells in Column B (starting from B2)
2. Data → Data Validation → Allow: List
3. Source: `Fixed,Variable,Discretionary`

---

## Sheet 2: Category Summary

### Column Structure

| Column | Header | Formula |
|--------|--------|---------|
| A | **Category** | Fixed values |
| B | **Total (THB)** | SUMIF formula |
| C | **Percentage** | Percentage of total |
| D | **Daily Average** | Divide by days tracked |

### Data & Formulas

| A (Category) | B (Total) | C (Percentage) | D (Daily Average) |
|--------------|-----------|----------------|-------------------|
| Fixed | `=SUMIF(DailyTracker!B:B,"Fixed",DailyTracker!D:D)` | `=B2/B$5` | `=B2/60` |
| Variable | `=SUMIF(DailyTracker!B:B,"Variable",DailyTracker!D:D)` | `=B3/B$5` | `=B3/60` |
| Discretionary | `=SUMIF(DailyTracker!B:B,"Discretionary",DailyTracker!D:D)` | `=B4/B$5` | `=B4/60` |
| **TOTAL** | `=SUM(B2:B4)` | `=SUM(C2:C4)` | `=SUM(D2:D4)` |

### Budget vs Actual

| Column | Header | Formula |
|--------|--------|---------|
| E | **Budget (THB)** | Manual entry |
| F | **Actual (THB)** | Link to B |
| G | **Difference** | Budget minus Actual |
| H | **Status** | IF formula |

| E (Budget) | F (Actual) | G (Difference) | H (Status) |
|------------|------------|----------------|------------|
| 6,000 | `=B2` | `=E2-F2` | `=IF(G2>=0,"✅ Under","❌ Over")` |
| 8,000 | `=B3` | `=E3-F3` | `=IF(G3>=0,"✅ Under","❌ Over")` |
| 6,000 | `=B4` | `=E4-F4` | `=IF(G4>=0,"✅ Under","❌ Over")` |
| 20,000 | `=B5` | `=E5-F5` | `=IF(G5>=0,"✅ Under","❌ Over")` |

---

## Sheet 3: Monthly Summary

### Column Structure

| Column | Header | Format |
|--------|--------|--------|
| A | **Month** | Date (YYYY-MM) |
| B | **Income** | Number |
| C | **Total Expenses** | Formula |
| D | **Surplus/Deficit** | Formula |
| E | **Savings Rate** | Formula |
| F | **Cumulative Savings** | Formula |

### Data & Formulas

| A (Month) | B (Income) | C (Expenses) | D (Surplus) | E (Savings Rate) | F (Cumulative) |
|-----------|------------|--------------|-------------|------------------|----------------|
| 2025-01 | 32,000 | `=SUMIF(DailyTracker!A:A,">="&DATE(2025,1,1),DailyTracker!D:D)-SUMIF(DailyTracker!A:A,">"&DATE(2025,2,1),DailyTracker!D:D)` | `=B2-C2` | `=D2/B2` | `=D2` |
| 2025-02 | 32,000 | *(same pattern)* | `=B3-C3` | `=D3/B3` | `=F2+D3` |
| 2025-03 | 32,000 | *(same pattern)* | `=B4-C4` | `=D4/B4` | `=F3+D4` |

### Simplified Version (Manual Entry)

If the SUMIF dates are too complex, use this simpler approach:

| A (Month) | B (Income) | C (Expenses) | D (Surplus) | E (Savings Rate) | F (Cumulative) |
|-----------|------------|--------------|-------------|------------------|----------------|
| 2025-01 | 32,000 | 18,500 | `=B2-C2` | `=D2/B2` | `=D2` |
| 2025-02 | 32,000 | 19,200 | `=B3-C3` | `=D3/B3` | `=F2+D3` |
| 2025-03 | 32,000 | 17,800 | `=B4-C4` | `=D4/B4` | `=F3+D4` |

*Just copy the total expenses from Sheet 2 each month.*

---

## Sheet 4: Emergency Fund Tracker

### Column Structure

| Column | Header | Formula/Value |
|--------|--------|---------------|
| A | **Month** | Date |
| B | **Deposit** | Manual entry |
| C | **Withdrawal** | Manual entry |
| D | **Balance** | Formula |
| E | **Progress** | Formula |
| F | **Status** | Formula |

### Data & Formulas

| A (Month) | B (Deposit) | C (Withdrawal) | D (Balance) | E (Progress) | F (Status) |
|-----------|-------------|----------------|-------------|--------------|------------|
| 2025-03 | 10,000 | 0 | `=SUM(B$2:B2)-SUM(C$2:C2)` | `=D2/60000` | `=IF(E2>=1,"✅ COMPLETE",IF(E2>=0.75,"🟡 75%+",IF(E2>=0.5,"🟡 50%+","🔵 Building")))` |
| 2025-04 | 10,000 | 0 | `=SUM(B$2:B3)-SUM(C$2:C3)` | `=D3/60000` | `=IF(E3>=1,"✅ COMPLETE",IF(E3>=0.75,"🟡 75%+",IF(E3>=0.5,"🟡 50%+","🔵 Building")))` |
| 2025-05 | 10,000 | 0 | `=SUM(B$2:B4)-SUM(C$2:C4)` | `=D4/60000` | `=IF(E4>=1,"✅ COMPLETE",IF(E4>=0.75,"🟡 75%+",IF(E4>=0.5,"🟡 50%+","🔵 Building")))` |
| 2025-06 | 10,000 | 0 | `=SUM(B$2:B5)-SUM(C$2:C5)` | `=D5/60000` | `=IF(E5>=1,"✅ COMPLETE",IF(E5>=0.75,"🟡 75%+",IF(E5>=0.5,"🟡 50%+","🔵 Building")))` |

### Conditional Formatting

Apply to Column E (Progress):
- **Green:** `E >= 1` (100% or more)
- **Yellow:** `E >= 0.5` (50% or more)
- **Blue:** `E < 0.5` (under 50%)

---

## Sheet 5: Investment Tracker

### Column Structure

| Column | Header | Description |
|--------|--------|-------------|
| A | **Asset Class** | RMF / SSF / SET50 / Stock / Crypto |
| B | **Allocation %** | Target allocation |
| C | **Monthly Amount** | Formula |
| D | **Total Invested** | Running total |
| E | **Current Value** | Manual update |
| F | **Return %** | Formula |
| G | **Notes** | Any notes |

### Data & Formulas

| A (Asset) | B (Allocation) | C (Monthly) | D (Total Invested) | E (Current Value) | F (Return) | G (Notes) |
|-----------|----------------|-------------|--------------------|--------------------|------------|-----------|
| RMF | 50% | `=10000*B2` | `=SUM(RMFDaily!B:B)` | *(update monthly)* | `=(E2-D2)/D2` | Tax benefit |
| SSF | 30% | `=10000*B3` | `=SUM(SSFDaily!B:B)` | *(update monthly)* | `=(E3-D3)/D3` | Tax benefit |
| SET50 Index | 20% | `=10000*B4` | `=SUM(SET50Daily!B:B)` | *(update monthly)* | `=(E4-D4)/D4` | Diversified |

### Portfolio Summary

| Metric | Formula |
|--------|---------|
| Total Invested | `=SUM(D2:D4)` |
| Current Value | `=SUM(E2:E4)` |
| Total Return | `=F5-F4` |
| Overall Return % | `=(E5-D5)/D5` |

---

## Sheet 6: Budget Planner (50/30/20 Rule)

### Structure

| A (Category) | B (Percentage) | C (Amount) | D (Actual) | E (Difference) | F (Status) |
|--------------|----------------|------------|------------|----------------|------------|
| **Needs (50%)** | | | | | |
| Health Insurance | | `=32000*0.125` | *(from tracker)* | `=C3-D3` | `=IF(E3>=0,"✅","❌")` |
| Rent/Housing | | `=32000*0.125` | *(from tracker)* | `=C4-D4` | `=IF(E4>=0,"✅","❌")` |
| Food | | `=32000*0.15` | *(from tracker)* | `=C5-D5` | `=IF(E5>=0,"✅","❌")` |
| Transport | | `=32000*0.1` | *(from tracker)* | `=C6-D6` | `=IF(E6>=0,"✅","❌")` |
| **Wants (30%)** | | | | | |
| Entertainment | | `=32000*0.1` | *(from tracker)* | `=C8-D8` | `=IF(E8>=0,"✅","❌")` |
| Shopping | | `=32000*0.1` | *(from tracker)* | `=C9-D9` | `=IF(E9>=0,"✅","❌")` |
| Dining Out | | `=32000*0.1` | *(from tracker)* | `=C10-D10` | `=IF(E10>=0,"✅","❌")` |
| **Savings (20%)** | | | | | |
| Emergency Fund | | `=32000*0.1` | *(from tracker)* | `=C12-D12` | `=IF(E12>=0,"✅","❌")` |
| Investment | | `=32000*0.1` | *(from tracker)* | `=C13-D13` | `=IF(E13>=0,"✅","❌")` |

---

## Sheet 7: Annual Overview

### Structure

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| **Year** | **Total Income** | **Total Expenses** | **Total Saved** | **Savings Rate** | **Emergency Fund** | **Investments** | **Net Worth** |
| 2025 | `=SUM(MonthlySummary!B:B)` | `=SUM(MonthlySummary!C:C)` | `=SUM(MonthlySummary!D:D)` | `=D2/B2` | *(from EF tracker)* | *(from invest tracker)* | `=F2+G2` |

---

## 📋 Quick Reference: All Formulas

### Daily Tracker (Sheet 1)
```
Running Total (E2): =SUM(D$2:D2)
```

### Category Summary (Sheet 2)
```
Fixed Total: =SUMIF(DailyTracker!B:B,"Fixed",DailyTracker!D:D)
Variable Total: =SUMIF(DailyTracker!B:B,"Variable",DailyTracker!D:D)
Discretionary Total: =SUMIF(DailyTracker!B:B,"Discretionary",DailyTracker!D:D)
Grand Total: =SUM(B2:B4)
```

### Monthly Summary (Sheet 3)
```
Surplus: =B2-C2
Savings Rate: =D2/B2
Cumulative: =SUM(D$2:D2)
```

### Emergency Fund (Sheet 4)
```
Balance: =SUM(B$2:B2)-SUM(C$2:C2)
Progress: =D2/60000
Status: =IF(E2>=1,"✅ COMPLETE",IF(E2>=0.75,"🟡 75%+",IF(E2>=0.5,"🟡 50%+","🔵 Building")))
```

### Investment (Sheet 5)
```
Monthly Amount: =Total_Investment * B/100
Return %: =(Current_Value - Total_Invested)/Total_Invested
```

---

## 🎨 Conditional Formatting Rules

### Daily Tracker
- Column D (Amount): Red if > 1000 THB

### Monthly Summary
- Column D (Surplus): Green if > 0, Red if < 0
- Column E (Savings Rate): Green if > 20%, Yellow if > 10%, Red if < 10%

### Emergency Fund
- Column E (Progress): Green if >= 1, Yellow if >= 0.5, Blue if < 0.5

### Budget Planner
- Column F (Status): Already uses IF formula for ✅/❌

---

## 📱 Daily Tracking Checklist

Use this quick reference every day:

- [ ] Morning: Check if any fixed expenses today (insurance, subscriptions)
- [ ] After each purchase: Open tracker, add entry immediately
- [ ] Evening: Review day's expenses, check if any missed
- [ ] Weekly: Calculate weekly total, compare to last week

---

> **Remember:** The best tracker is the one you actually use. Start simple, stay consistent.

---

*Last Updated: __________*