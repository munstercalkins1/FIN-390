# Lab 09 — Pro-Forma Build: the Engine and the Known Answer

## Question

What are five years of a company's statements worth when they are built from defensible assumptions, and how can the statements be checked?

## The three value-carrying judgments

The ABG model is especially driven by organic revenue growth (1.8% a year), gross margin (17.05%), and SG&A as a percentage of gross profit (66.5% in 2026, declining to 64.5%). Revenue growth determines the scale of future earnings and inventory needs. Gross margin determines the gross-profit pool available to cover operating costs. The SG&A ratio determines how much of that pool becomes operating income. Changes in any of these assumptions flow through net income, working capital, free cash flow to equity, and value per share.

Cash is computed last because it is the outcome of the operating forecast, investment spending, working-capital movement, debt repayment, and share repurchases. It is not an independent assumption. If the model needs cash below the $25 million minimum, it draws the revolver; if it has excess cash, it repays the revolver first.

## Model and validation

`proforma.py` projects ABG's income statement, balance sheet, and free cash flow to equity from 2026 through 2030. It calculates revenue, margins, operating costs, interest, taxes, working capital, floor-plan financing, capital spending, debt, equity, and cash in the required sequence.

The model reproduces the known answer to one decimal:

| Line | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| Free cash flow to equity | 211.4 | 342.3 |
| Cash, year end | 101.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 |

The equity valuation is **$291.75 per share**. The present value of cash flows after 2030 is about **79.8%** of total equity value.

The `assert_balanced` function raises an error naming the year and the balance-sheet gap when assets do not equal liabilities plus equity. Replacing FY2026E cash of 101.8 with the opening cash balance of 40.4 produces a **−61.4** gap, so the model refuses the broken statement.

## Floor-plan financing

Floor-plan financing is inventory debt provided by manufacturers' finance arms or banks to automobile dealerships. Because it finances vehicles held for sale, it rises as inventory rises and falls as inventory falls. The model calculates interest on the opening floor-plan balance and includes its year-over-year movement in FCFE. Removing the line would force the dealership to fund its inventory with cash, which is why the video shows cash falling to roughly negative $1.1 billion.

## Submission

Submit GitHub links to `proforma.py` and this file after running the model in the course environment and confirming the printed checks.
