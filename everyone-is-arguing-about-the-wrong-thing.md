# Everyone Is Arguing About the Wrong Thing

### In one week of September 2026, the people building artificial intelligence asked to be slowed down, the president called it a hoax, and a kernel engineer in China explained why both of them might be missing the point

**Joseph Catanzarite**, with Claude Opus 5 (extra-high reasoning effort, extended thinking enabled) as research partner.

*The full report carries the citations, the contested readings, and the claims that remain unverified.*

---

On Saturday, September 12, 2026, Dario Amodei, who runs Anthropic, published roughly thirty-five hundred words arguing that his own industry was moving too fast. Not a pause — he is explicit about the distinction — but a deliberate slowing of the rate at which frontier models get more capable. Sam Altman, who runs OpenAI, agreed the same day. Elon Musk agreed in three words: "Dario is right." Three days after that, Congress left for the midterms without holding a vote.

That consensus is hard to take at face value.

Start with the calendar. Anthropic was weeks from marketing the largest initial public offering in American history, at a valuation approaching $2 trillion, timed to list days before the November midterms. OpenAI had its own filing in a drawer. The men asking the industry to decelerate were, in the same month, asking public investors to price acceleration.

Then consider what happened four days earlier. A 27-year-old Anthropic researcher named Jacob Coxon resigned, forfeited unvested equity to do it, and posted that neither his employer nor OpenAI was acting responsibly. Anthropic's alignment science lead answered him on the record: "We really do earnestly believe AI could kill all humans," with a personal estimate above 10% within the decade. The essay landed in an argument already under way.

The obvious reading is that an industry discovered its conscience. The obvious counter-reading is that an industry discovered a regulatory moat. Both are too clean, and both miss the more interesting problem: almost everyone in this argument is arguing along the wrong axis.

## Two nightmares, not one

The debate gets framed as safety versus acceleration — the cautious against the reckless. That framing survives about ten minutes of contact with the actual positions.

Around the same week, a kernel engineer at the Chinese lab DeepSeek published an essay of his own — in Chinese, and read here in translation, which is worth saying before summarizing a man's argument for him. Shengyu Liu wrote the main attention kernel for DeepSeek's V4.1 model, which is to say he does the kind of low-level optimization work that was supposed to be the last thing automated. He describes watching AI close the distance on his own craft inside a single year, and expects to be matched within six to twelve months. He keeps working, because his competitors will keep working regardless of what he decides.

Liu is not an accelerationist. He thinks frontier AI is dangerous. He simply disagrees with Amodei about *which* danger dominates — and that disagreement generates opposite policies.

Amodei's nightmare is misuse or loss of control, and his remedy requires capability concentrated in a few auditable actors, because you cannot inspect what you cannot locate. Liu's nightmare is a permanent capability aristocracy, and his remedy requires capability cheap and universal, accepting more misuse as the price of preventing a narrow elite from owning the future outright.

Run the policies and they invert cleanly. Amodei wants inspectors embedded inside the labs; Liu sees unaccountable private authority handpicked by the firms. Amodei wants chip export controls sustained; Liu sees the American lead they produce as the problem itself. Amodei wants a crackdown on distillation — training a cheap model to imitate an expensive one — which is precisely how Chinese labs stay close. Both men have real technical standing. Both are making a safety argument. They are not on the same axis at all.

The axis they are actually on is concentration versus diffusion, and it is the one nobody in power is debating.

## Nobody outside the building can check any of this

The frontier is going dark to outside measurement, through at least four mechanisms that arrived separately and compound. Anthropic released two models on September 1, 2026. Fable 5.1 is public. Mythos 5.1 is restricted, and was withheld from pre-release testing by Britain's AI Security Institute — the first such exclusion on record, of an allied government's own safety body. The detail that matters is smaller than the exclusion: Fable and Mythos are the same underlying model, and Fable simply carries additional safeguards. Every benchmark number anyone outside Anthropic has ever seen for this generation is a Fable number.

Meanwhile, California's Senate Bill 53 — the most substantial artificial-intelligence statute in the country — defines a "frontier developer" as one training above 10²⁶ operations, and leaves that determination to the developer. There is no public register of which models cross the line, and none can be built. The law's incident reports are exempt from public-records requests, with anonymized summaries not due until January 2027.

The effect compounds. Confident claims about which American lab is ahead rest on comparing a deliberately safeguarded model against an unconstrained rival, using aggregator scores that contradict each other — Fable 5.1's score on one industry index was reported as both first and third place by different sources six days apart.

That quietly destroys the most popular cynical explanation of the whole affair. The clever reading of Amodei's essay is that a pacing regime freezes the board in favor of whoever currently leads, so the call should have come from the leader. Running that test requires knowing who leads. Nobody outside either building does, and the release policies are designed so that nobody will. The observation that the "wrong" man wrote the essay carries no evidential weight at all, because it would look identical in either world.

## What actually costs something

If motives can't be read from essays, they can sometimes be read from bills.

In early 2026 the Pentagon sought to renegotiate its contract with Anthropic to permit use of Claude, the company's AI model, "for all lawful purposes" — dropping the company's red lines against mass domestic surveillance and autonomous weapons targeting. Anthropic refused. The administration directed every federal agency to phase the company out, and the Defense Secretary designated it a "supply chain risk," a label never before applied to an American firm. OpenAI took a comparable contract with softer, self-amendable protections.

In August, a federal judge ruled the designation unlawful on three grounds at once, finding the government had acted "based on a desire to make a public example." A second suit continues.

That episode is the single most useful fact in this story, because it is the only one where a party paid a real price for a position. Essays are free. Agreeing with an essay is free. Absorbing an unprecedented federal blacklist rather than dropping a contractual red line is not free, and it happened.

It also suggests the right question. "Is Amodei sincere?" cannot be answered from public evidence and probably never will be. "Under what conditions does a firm give up money when nothing forces it to?" is answerable, because it is about conduct. The Pentagon refusal is one entry. The discipline worth keeping is to collect more of them, and to stop treating stated motives as data.

Applied evenly, that discipline is unkind to everyone. Amodei's proposal happens to formalize compliance infrastructure Anthropic already built and its rivals mostly have not. Liu's argument concludes that the correct policy is exactly what his employer already does, and exactly what keeps his own threatened craft meaningful. Neither observation makes either man insincere. Sincere and self-serving have never been mutually exclusive.

## The money runs in both directions

The political economy is usually described as tech money flowing toward the president. It does. Federal Election Commission records show that OpenAI co-founder Greg Brockman and his wife Anna gave $50 million on a single day in September 2025 — four contributions of $12.5 million each, half to the president's super political action committee and half to the industry's deregulation network. Media and technology companies have paid Trump roughly $90 million in lawsuit settlements as announced, most of it routed to his presidential library foundation.

What gets less attention is the flow in the opposite direction, and Senator Jon Ossoff laid it out in a four-step sequence at a rally in Athens, Georgia on September 13. On day one of the administration, the Biden executive order guarding against catastrophic AI risks was rescinded. Donald Trump Jr.'s venture firm, 1789 Capital, took positions in data centers and AI labs — its portfolio includes a data-center operator and a chip designer, and its assets under management grew from roughly $200 million to $3.5 billion in a year. Four days before the inauguration, a group led by the United Arab Emirates' national security adviser committed $500 million to the Trump family's crypto venture; the president's own financial disclosure indicates the arrangement has since directed $263 million to family entities. Four months later, the administration signed the framework granting the Emirates the right to buy up to half a million advanced Nvidia chips a year.

Each step checks out against the public record, with one correction worth making: the framework granting purchase rights came in May 2025, but the export licenses themselves arrived months afterward.

The structural point survives the correction. A president whose family holds positions in an industry has a reason not to regulate it that owes nothing to lobbying, tribute, or capture. That reason runs from Washington toward the industry rather than the other way, and the standard account of tech money flowing to the president leaves it out entirely.

## What a functioning response would look like

At the same rally Ossoff set out a standard, and its construction is the substance of it. He does not say what he would do. He says what the offices would do if the people in them were equal to them.

"A capable president," in his formulation, "would move swiftly to secure and reassure the American people, rush inspectors into frontier labs, fortify the nation against bioterrorism, demand legislation from Congress, and lead the world toward an AI treaty." A capable Congress "would engage every committee in investigation and legislation to act swiftly and wisely," and the relevant chief executives "would be under oath next week." Only then the measurement: "But instead the president and the speaker of the house sit on their hands and hope for the best."

Read as a job description, that assigns six duties to the executive and three to the legislature, and holds both to the same twin standard — swiftly *and* wisely. Elsewhere he names the two components directly, describing what he hopes to tell his daughter her parents' generation did: that "we elected those who understood the moment and had the will to meet it." Comprehension and will are exactly the two things his critique says are missing, from an establishment "barely capable of email" and a president whose family holds positions in the industry.

The answer came quickly. Trump posted that the AI crisis was a "hoax being perpetrated by the radical left Democrats," comparing it to climate change. The Senate majority leader said Congress should take a "light touch" with AI companies. The Speaker said the industry could "self-regulate" and did not need government "to tell them to slow it down." That week was the House's last scheduled sitting before the midterms, which closed the legislative window for the year.

Two days later, several hundred people met in Washington under a banner that fits no partisan axis at all. Bernie Sanders and Steve Bannon shared a stage demanding binding limits on AI, which does not survive the "radical left Democrats" framing. Their prescriptions have almost nothing in common. But the president of the American Federation of Labor and Congress of Industrial Organizations was on that stage, alongside the head of the American Federation of Teachers and the executive director of the screen actors' union. Organized labor has entered this argument, and entered it on displacement rather than extinction. That is a different fight, with a far larger constituency than the one the laboratories have been having with themselves.

## What to watch

Strip the week down and four things hold. The loudest calls for restraint came from the firms setting the pace, in the same weeks they pursued the largest public offerings in history, from a government that rejects restraint while collecting money from the industry it regulates. Nobody in the story is a neutral party to their own regulation, and that is the only frame that fits all the conduct at once.

The chokepoint that makes any of this governable is tightening on the creation side and eroding on the diffusion side, and every proposal on the table addresses the half that is tightening. Compute concentration makes inspections feasible. Open weights and distillation make containment nearly impossible. Amodei's package is well matched to the easy half.

The measurable facts are becoming scarcer while the claims get louder. Release policy, self-assessed compute thresholds, and sealed incident reports mean the most important questions — who is actually ahead, what actually went wrong inside a lab — are now structurally unanswerable from outside.

And the argument that matters is not the one being had. Concentration versus diffusion is the axis that explains why a senator, a chief executive, and a Chinese kernel engineer can all invoke safety and demand incompatible things. Ossoff named five duties for a functioning government: inspectors, testimony, biosecurity, legislation, a treaty. As of this writing, none of the five has happened, and Congress has gone home.
