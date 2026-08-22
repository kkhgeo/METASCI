import numpy as np
from figspec import Spec
rng=np.random.default_rng(7); S=Spec.load("figure_spec.yaml")
def synth(n, lo, hi, f):
    ec=rng.uniform(lo,hi,n); return ec, np.clip(f(ec)+rng.normal(0,0.08*np.abs(f(ec)).max()+0.5,n),0,None)
groups={"A":{"impacted":20,"background":28},"B":{"impacted":21,"background":39},"C":{"impacted":19,"background":49}}
def draw(ax, pid, ylab, f, legend=False):
    T={"x":"EC (μS/cm)","y":ylab,"impacted":"LMWs","background":"BGWs"}
    for site,gs in groups.items():
        for role,n in gs.items():
            x,y=synth(n,*((500,2400) if role=="impacted" else (100,550)),f)
            ax.plot(x,y,ls="none",marker=S.site_marker(site),color=S.color(role),
                    label=f"{T[role]} {site}" if legend else None,**S.marker())
    ax.set_xlim(0,2500); ax.set_xlabel(T["x"]); ax.set_ylabel(T["y"])
    if legend: S.legend(ax,pid,ncol=2)
    S.annotate(ax,pid); S.style(ax,pid)
fig=S.canvas()
draw(S.panel(fig,"a"),"a","NH₄⁺ (mg/L)",lambda e:np.where(e>700,(e-700)*0.12,0))
draw(S.panel(fig,"b"),"b","NO₃⁻ (mg/L)",lambda e:np.clip(160-0.1*e,0,None),legend=True)
draw(S.panel(fig,"c"),"c","Fe + Mn (mg/L)",lambda e:np.where(e>700,(e-700)*0.01,0.2))
draw(S.panel(fig,"d"),"d","SO₄²⁻ (mg/L)",lambda e:np.clip(60-0.02*e,5,None))
S.save(fig,"fig2_new")
