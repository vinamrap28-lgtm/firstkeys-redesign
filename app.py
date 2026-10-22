"""FirstKeys — polished Streamlit prototype. Run: streamlit run app.py"""
import datetime as dt
import os
from pathlib import Path
import pandas as pd
import streamlit as st
import pipeline as pl

st.set_page_config(page_title="firstkeys | Smarter matches. Better moves.", page_icon="🏠", layout="wide", initial_sidebar_state="collapsed")
BASE = Path(__file__).parent
LEADS = BASE / "data" / "live_leads.csv"
LOGO = BASE / "assets_logo.png"
BLURB = {
    "Ready-to-Move Maker": "You're financially and mentally ready. The next step is a shortlist and a site visit.",
    "The Active Planner": "You're actively researching. Comparing options, pricing and payment plans will help most.",
    "The Smart Saver": "You want to own a home but there's a savings gap. Budget-friendly options and a savings plan fit best.",
    "The Vibe Seeker": "Neighbourhood, amenities and lifestyle fit matter most to you.",
    "The Future Builder": "You're thinking long-term: appreciation and locality growth matter.",
    "The Early Explorer": "You're early in your journey. Take your time; there's no pressure to decide yet.",
}
# Sample editorial imagery from Unsplash. These are illustrative photos, not verified project photos.
PROPERTY_IMAGES = [
    "https://images.unsplash.com/photo-1460317442991-0ec209397118?auto=format&fit=crop&w=1000&q=85",
    "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1000&q=85",
    "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1000&q=85",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1000&q=85",
]
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--fk-orange:#ff6b1a;--fk-ink:#191a1d;--fk-muted:#69707b;--fk-line:#ececf0;--fk-cream:#fffaf5;}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--fk-ink)}
.stApp{background:radial-gradient(ellipse at 12% 0%,#fff1e7 0%,transparent 32%),linear-gradient(135deg,#fbfcff 0%,#fffaf5 60%,#f6f8ff 100%)}
.block-container{max-width:1380px;padding-top:1rem;padding-bottom:3rem}
header[data-testid="stHeader"]{background:rgba(255,255,255,.55)}
section[data-testid="stSidebar"]{background:#fffaf6;border-right:1px solid #f1e7df}
h1,h2,h3{font-family:'Manrope',sans-serif;letter-spacing:-.035em!important}
h1{font-weight:800!important} h2{font-weight:800!important} h3{font-weight:750!important}
.eyebrow{color:var(--fk-orange);font-size:.78rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase}
.hero{padding:1.35rem 1.5rem;border:1px solid rgba(255,255,255,.9);border-radius:26px;background:linear-gradient(120deg,rgba(255,255,255,.94),rgba(255,246,238,.85));box-shadow:0 12px 35px rgba(32,38,55,.06);margin-bottom:1.1rem}
.card{padding:1rem 1.1rem;border-radius:22px;background:rgba(255,255,255,.88);border:1px solid rgba(255,255,255,.95);box-shadow:0 8px 24px rgba(31,41,55,.055);margin-bottom:.75rem}
.score{font-family:'Manrope',sans-serif;font-size:3rem;line-height:1;font-weight:800;letter-spacing:-.06em;color:var(--fk-ink)}
.score small{font-size:1rem;color:var(--fk-muted);font-weight:600;letter-spacing:0}
.pill{display:inline-block;padding:.35rem .7rem;border-radius:999px;background:#fff0e6;color:#e95b0b;font-size:.78rem;font-weight:700}
.reason{background:linear-gradient(90deg,#fff6df,#eef9ed);border-radius:12px;padding:.65rem .75rem;font-size:.86rem;color:#34423a}
div.stButton>button[kind="primary"]{background:linear-gradient(100deg,#ff7a1a,#ff5b0a);border:0;border-radius:999px;color:white;font-weight:700;min-height:2.8rem;box-shadow:0 6px 15px #ff6b1a2b}
div.stButton>button{border-radius:999px;font-weight:650;border-color:#e7e7eb}
[data-testid="stMetric"]{background:white;border:1px solid #f0eff2;padding:1rem;border-radius:18px;box-shadow:0 5px 16px #1f29370a}
[data-testid="stProgressBar"]>div>div{background:linear-gradient(90deg,#ff9b3d,#ff5b0a)}
[data-testid="stTabs"] button{border-radius:999px!important;padding:.55rem 1rem!important}
hr{border-color:#eeedf0}
@media(max-width:800px){.block-container{padding-left:1rem;padding-right:1rem}.score{font-size:2.4rem}}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load():
    return pl.run_all(str(BASE / "data" / "buyers_raw.csv"), str(BASE / "data" / "properties_raw.csv"))
R = load(); b, p, m = R["buyers"], R["properties"], R["matches"]

with st.sidebar:
    if LOGO.exists(): st.image(str(LOGO), width=180)
    else: st.markdown("# <span style='color:#ff6b1a'>firstkeys</span>", unsafe_allow_html=True)
    st.caption("Smarter matches. Better moves.")
    mode = st.radio("Choose your experience", ["Buyer view", "Builder view"], horizontal=False)
    st.divider()
    st.caption("Prototype uses synthetic buyer and property data. Scores are decision-support signals, not loan approval or purchase predictions.")

# Shared header
left, right = st.columns([4,1])
with left:
    st.markdown('<div class="eyebrow">Your next chapter starts here</div>', unsafe_allow_html=True)
    st.title("Smarter matches. Better moves.")
    st.caption("A first-home journey designed around your money, your lifestyle and your timing.")
with right:
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='pill'>BETA · FIRSTKEYS</div>", unsafe_allow_html=True)

if mode == "Buyer view":
    st.markdown('<div class="hero"><div class="eyebrow">Buyer view</div><h2 style="margin:.2rem 0">Let’s find a home that fits you.</h2><div style="color:#69707b">Tell us what matters. We’ll help you understand your readiness and shortlist homes that fit.</div></div>', unsafe_allow_html=True)
    tab_profile, tab_results, tab_sim, tab_share = st.tabs(["① Your profile", "② Your matches", "③ What-if simulator", "④ Share with builder"])
    with tab_profile:
        st.markdown("### Start with the essentials")
        a,bcol = st.columns(2, gap="large")
        with a:
            st.markdown('<div class="card"><div class="eyebrow">01 · Your money</div>', unsafe_allow_html=True)
            age = st.slider("Age", 21, 30, 25)
            income = st.slider("Annual income (₹ LPA)", 2, 40, 12)
            savings = st.slider("Savings for down payment (₹ lakh)", 0, 60, 12)
            budget = st.slider("Home budget (₹ lakh)", 25, 400, 80, step=5)
            st.caption(f"Down-payment cover: **{savings / budget:.0%}** of budget · Budget = **{budget / income:.1f}×** annual income")
            timeline = st.select_slider("When do you want to buy?", ["0-3 months", "3-6 months", "6-12 months", "12+ months", "Not sure"], "6-12 months")
            motive = st.radio("Why are you buying?", ["Self-use", "Investment", "Both"], horizontal=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with bcol:
            st.markdown('<div class="card"><div class="eyebrow">02 · Your home & lifestyle</div>', unsafe_allow_html=True)
            city = st.selectbox("Preferred city", ["Not sure yet"] + sorted(p.city.dropna().unique().tolist()))
            locs = ["Flexible"] + (sorted(p[p.city == city].locality.dropna().unique().tolist()) if city != "Not sure yet" else [])
            locality = st.selectbox("Preferred locality", locs)
            ptype = st.selectbox("Property type", ["Any", "Apartment", "Builder Floor", "Villa"])
            bhk = st.selectbox("BHK", ["Any", 1, 2, 3, 4], index=2)
            amen = st.multiselect("Lifestyle must-haves", pl.AMENITIES, [x for x in ["WFH Space", "Gym"] if x in pl.AMENITIES])
            site = st.checkbox("I’d like a site visit")
            brochure = st.checkbox("I’d like a brochure")
            st.markdown('</div>', unsafe_allow_html=True)
        prof = dict(age=age, income_lpa=income, savings_lakh=savings, budget_lakh=budget, timeline=timeline, motive=motive, city=city, locality=locality, ptype=ptype, bhk=bhk, amenities=amen, site_visit=site, brochure=brochure)
        r, mm = pl.score_single(prof, p)
        st.markdown("### Your Move-In Meter, updated live")
        c1,c2,c3 = st.columns([1,1.4,1])
        with c1:
            st.markdown(f"<div class='card'><div style='color:#69707b;font-weight:700'>MOVE-IN METER</div><div class='score'>{r.move_in_score:.0f}<small> / 100</small></div><div class='pill'>{r.readiness_level} readiness</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='card'><div style='color:#69707b;font-weight:700'>YOUR PERSONA</div><h3 style='margin:.5rem 0'>{r.persona}</h3><div>{BLURB.get(r.persona, 'Explore the homes that fit your priorities.')}</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='card'><div style='color:#69707b;font-weight:700'>AFFORDABILITY</div><h3 style='margin:.5rem 0'>{r.affordability}</h3><div style='color:#69707b;font-size:.85rem'>A planning signal, not a lending decision.</div></div>", unsafe_allow_html=True)
        st.progress(min(max(float(r.move_in_score),0),100)/100)
        with st.expander("How is my Move-In Meter calculated?"):
            st.dataframe(pd.DataFrame({"Your points":[r.pts_financial,r.pts_timeline,r.pts_engagement,r.pts_clarity],"Maximum points":[40,25,20,15]},index=["Financial capacity","Purchase timeline","Interest shown","Preference clarity"]), use_container_width=True)
    with tab_results:
        st.markdown("### Homes that match your profile")
        st.caption("Match scores compare budget, neighbourhood, space, lifestyle and timing fit.")
        ready_only = st.toggle("Only show ready-to-move homes", key="ready_only")
        r, mm = pl.score_single(prof, p)
        show = pl.match_buyers(pd.DataFrame([r]), p[p.possession_months == 0] if ready_only else p, 3) if ready_only else mm
        if show.empty: st.info("No matches found for these filters. Try broadening your budget, location or timeline.")
        for i,(_,x) in enumerate(show.iterrows()):
            with st.container(border=True):
                cimg, cinfo = st.columns([1,2.4], gap="large")
                with cimg: st.image(PROPERTY_IMAGES[i % len(PROPERTY_IMAGES)], use_container_width=True)
                with cinfo:
                    st.markdown(f"<div class='pill'>{x.home_match_score:.0f}% HOME MATCH</div>", unsafe_allow_html=True)
                    st.markdown(f"### {x.project_name}")
                    st.caption(f"📍 {x.locality}, {x.city}  ·  {x.bhk} BHK {x.property_type}")
                    st.markdown(f"**{pl.fmt_lakh(x.price_lakh)}**  ·  {x.possession_status}")
                    st.markdown(f"<div class='reason'>✦ {x.why}</div>", unsafe_allow_html=True)
                    st.caption(f"Budget {x.budget_fit:.0f}/35 · Area {x.neighbourhood_match:.0f}/25 · Space {x.space_fit:.0f}/15 · Lifestyle {x.vibe_fit:.0f}/15 · Timing {x.move_clock_fit:.0f}/10")
        st.caption("Sample listing imagery: Unsplash. Images are illustrative and are not verified photographs of the named developments.")
    with tab_sim:
        st.markdown("### Try a what-if scenario")
        st.write("Explore how a different budget or buying timeline may change your readiness and best-fit homes.")
        wi1, wi2 = st.columns(2)
        with wi1:
            alt_budget = st.slider("Try a different budget (₹ lakh)",25,400,int(budget),step=5)
        with wi2:
            alt_timeline = st.selectbox("Try a different timeline",["0-3 months","3-6 months","6-12 months","12+ months","Not sure"],index=["0-3 months","3-6 months","6-12 months","12+ months","Not sure"].index(timeline))
        alt_prof = dict(prof); alt_prof["budget_lakh"] = alt_budget; alt_prof["timeline"] = alt_timeline
        ar, amm = pl.score_single(alt_prof,p)
        k1,k2,k3 = st.columns(3)
        k1.metric("Current Move-In Meter",f"{r.move_in_score:.0f}/100")
        k2.metric("Scenario Move-In Meter",f"{ar.move_in_score:.0f}/100",f"{ar.move_in_score-r.move_in_score:+.0f} points")
        k3.metric("Scenario persona",ar.persona)
        st.markdown("#### Best match in this scenario")
        if not amm.empty:
            x=amm.iloc[0]; ci,ct=st.columns([1,2.4])
            with ci: st.image(PROPERTY_IMAGES[0],use_container_width=True)
            with ct:
                st.markdown(f"### {x.project_name}")
                st.markdown(f"**{pl.fmt_lakh(x.price_lakh)}** · {x.locality}, {x.city} · **{x.home_match_score:.0f}% match**")
                st.write(x.why)
        st.caption("Scenario results are estimates from the prototype’s scoring rules, not financial advice or a loan decision.")
    with tab_share:
        st.markdown("### Share your profile with a builder")
        st.write("Share your preferences and match summary so a sales team can follow up with relevant homes instead of generic brochures.")
        st.info("Only share details you are comfortable sending to the builder’s sales team. This prototype stores shared profiles in a local CSV file.")
        ok = st.checkbox("I agree to share this profile and results with the builder’s sales team.")
        if st.button("Share with builder",type="primary",disabled=not ok,use_container_width=True):
            now=dt.datetime.now()
            row={"lead_id":f"LIVE-{now:%m%d%H%M%S}","submitted_at":now.isoformat(timespec="seconds"),**{k:(";".join(v) if isinstance(v,list) else v) for k,v in prof.items()},"persona":r.persona,"move_in_score":r.move_in_score,"readiness_level":str(r.readiness_level),"top_match":f"{mm.project_name.iloc[0]} ({mm.property_id.iloc[0]})" if not mm.empty else "No match","top_match_score":mm.home_match_score.iloc[0] if not mm.empty else 0,"suggested_action":r.suggested_action}
            pd.DataFrame([row]).to_csv(LEADS,mode="a",header=not LEADS.exists(),index=False)
            st.success("Profile shared. The builder view can now review this lead and its best-fit homes.")
else:
    # Simple password gate; configure FIRSTKEYS_BUILDER_PASSWORD in deployment secrets/environment.
    expected=os.getenv("FIRSTKEYS_BUILDER_PASSWORD", st.secrets.get("FIRSTKEYS_BUILDER_PASSWORD", "firstkeys-demo"))
    if "builder_auth" not in st.session_state: st.session_state.builder_auth=False
    if not st.session_state.builder_auth:
        st.markdown('<div class="hero"><div class="eyebrow">Builder workspace</div><h2>Know who to follow up with first.</h2><div style="color:#69707b">A readiness-led view of shared buyer profiles and market demand.</div></div>',unsafe_allow_html=True)
        pwd=st.text_input("Builder password",type="password",help="Set FIRSTKEYS_BUILDER_PASSWORD in your deployment environment before publishing.")
        if st.button("Unlock builder view",type="primary"):
            if pwd==expected: st.session_state.builder_auth=True; st.rerun()
            else: st.error("That password didn’t match. Try again.")
        st.caption("Demo default is `firstkeys-demo`. Replace it in deployment settings before using real leads.")
    else:
        if st.button("Lock builder view"): st.session_state.builder_auth=False; st.rerun()
        f_persona=st.multiselect("Filter by persona",sorted(b.persona.dropna().unique()))
        f_ready=st.multiselect("Filter by readiness",["High","Medium","Early-stage"])
        f_city=st.multiselect("Filter by city",sorted(b.preferred_city.dropna().unique()))
        fb=b.copy()
        if f_persona: fb=fb[fb.persona.isin(f_persona)]
        if f_ready: fb=fb[fb.readiness_level.isin(f_ready)]
        if f_city: fb=fb[fb.preferred_city.isin(f_city)]
        t0,t1,t2,t3=st.tabs(["Live leads","Overview","Priority follow-up","Demand vs inventory"])
        with t0:
            st.markdown("### Live leads")
            if LEADS.exists():
                L=pd.read_csv(LEADS).sort_values("move_in_score",ascending=False)
                c=st.columns(3); c[0].metric("Shared profiles",len(L)); c[1].metric("High readiness",int((L.readiness_level=="High").sum())); c[2].metric("Average Move-In Meter",f"{L.move_in_score.mean():.0f}/100")
                st.dataframe(L[[x for x in ["lead_id","submitted_at","persona","move_in_score","readiness_level","city","budget_lakh","timeline","top_match","top_match_score","suggested_action"] if x in L.columns]],use_container_width=True,hide_index=True)
                st.download_button("Download leads CSV",L.to_csv(index=False),"firstkeys_live_leads.csv")
            else: st.info("No shared profiles yet. Switch to Buyer view and use Share with builder.")
        with t1:
            st.markdown("### Buyer overview")
            c=st.columns(4); c[0].metric("Profiles in view",len(fb)); c[1].metric("High readiness",int((fb.readiness_level=="High").sum())); c[2].metric("Average Move-In Meter",f"{fb.move_in_score.mean():.1f}" if len(fb) else "—"); c[3].metric("Average engagement",f"{fb.engagement_score.mean():.1f}" if len(fb) else "—")
            x,y=st.columns(2)
            with x: st.markdown("#### Buyer personas"); st.bar_chart(fb.persona.value_counts())
            with y: st.markdown("#### Readiness levels"); st.bar_chart(fb.readiness_level.value_counts())
            st.markdown("#### Most wanted amenities")
            s=fb[[f"want_{a}" for a in pl.AMENITIES]].sum(); s.index=pl.AMENITIES; st.bar_chart(s.sort_values(ascending=False))
        with t2:
            st.markdown("### Priority follow-up")
            st.caption("Ranked by Move-In Meter. Use as a decision-support queue, not an automatic sales decision.")
            st.dataframe(fb.sort_values("move_in_score",ascending=False)[["buyer_id","persona","move_in_score","readiness_level","budget_lakh","preferred_city","purchase_timeline","suggested_action"]].head(30),use_container_width=True,hide_index=True)
        with t3:
            st.markdown("### Demand vs inventory")
            st.caption("A positive gap indicates that buyer demand share exceeds inventory share.")
            for key,val in R["gaps"].items():
                st.markdown(f"#### {key}"); left,right=st.columns([1,1.4]); left.dataframe(val,use_container_width=True,hide_index=True); right.bar_chart(val.set_index(val.columns[0])[["demand_share","inventory_share"]])
        st.caption("Buyer records and analytics are synthetic unless explicitly shared through the live-lead flow. Configure persistent storage before production use.")

st.divider()
st.caption("© firstkeys · Prototype experience · Sample property images via Unsplash (illustrative only).")
