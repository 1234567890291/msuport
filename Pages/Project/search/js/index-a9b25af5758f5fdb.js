(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([[405], {
    4182: function(e, s, t) {
        (window.__NEXT_P = window.__NEXT_P || []).push(["/", function() {
            return t(404)
        }
        ])
    },
    404: function(e, s, t) {
        "use strict";
        t.r(s),
        t.d(s, {
            default: function() {
                return p
            }
        });
        var n = t(1527)
          , a = t(5377)
          , r = t.n(a)
          , l = t(1906)
          , i = t(959)
          , c = t(4480);
        let o = e => {
            let {toggle: s, isDark: t, setPost: a, post: r} = e
              , [o,d] = (0,
            i.useState)("")
              , u = async (e, s) => {
                e.preventDefault();
                let t = l.Z.request({
                    method: "GET",
                    url: "https://duckduckgo8.p.rapidapi.com/",
                    params: {
                        q: s
                    },
                    headers: {
                        "X-RapidAPI-Key": "f98e96f596msh9081e59d4bc3f09p19d9dejsn9d68dca27b60",
                        "X-RapidAPI-Host": "duckduckgo8.p.rapidapi.com"
                    }
                });
                try {
                    a((await t).data.results),
                    console.log(r)
                } catch (n) {
                    console.log(n)
                }
            }
            ;
            return (0,
            n.jsxs)("nav", {
                className: "mt-4 flex items-center justify-between px-4 md:px-12",
                children: [(0,
                n.jsx)("form", {
                    className: "form-control grow ",
                    onSubmit: e => u(e, o),
                    children: (0,
                    n.jsxs)("div", {
                        className: "input-group w-[90%] shadow-md md:w-[70%]",
                        children: [(0,
                        n.jsx)("input", {
                            type: "text",
                            value: o,
                            onChange: e => d(e.target.value),
                            placeholder: "Search With DitDev…",
                            className: "input-bordered input w-full focus:outline-none"
                        }), (0,
                        n.jsx)("button", {
                            type: "submit",
                            className: "btn-square btn",
                            children: (0,
                            n.jsx)("svg", {
                                xmlns: "http://www.w3.org/2000/svg",
                                className: "h-6 w-6",
                                fill: "none",
                                viewBox: "0 0 24 24",
                                stroke: "currentColor",
                                children: (0,
                                n.jsx)("path", {
                                    strokeLinecap: "round",
                                    strokeLinejoin: "round",
                                    strokeWidth: "2",
                                    d: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                                })
                            })
                        })]
                    })
                }), (0,
                n.jsx)("button", {
                    onClick: s,
                    className: "text-md btn col-span-1 grow-0",
                    children: t ? (0,
                    n.jsx)(c.UiM, {}) : (0,
                    n.jsx)(c.UYB, {})
                })]
            })
        }
          , d = e => {
            let {post: s} = e
              , t = s.map(e => (0,
            n.jsxs)("div", {
                className: "flex flex-col gap-2",
                children: [(0,
                n.jsx)("a", {
                    className: "link-hover link-secondary link text-lg",
                    target: "_blank",
                    href: e.url,
                    children: e.title
                }), (0,
                n.jsx)("p", {
                    className: "text-sm sm:text-base",
                    children: e.description
                })]
            }, e.position));
            return (0,
            n.jsx)("div", {
                className: "mt-12 flex max-w-2xl flex-col gap-8 px-8 md:px-20",
                children: t
            })
        }
        ;
        var u = t(5276);
        let m = () => {
            let[e,s] = (0,
            u._)("darkTheme", !0)
              , [t,a] = (0,
            i.useState)([])
              , l = () => {
                s(!e)
            }
            ;
            return (0,
            n.jsxs)(n.Fragment, {
                children: [(0,
                n.jsxs)(r(), {
                    children: [(0,
                    n.jsx)("title", {
                        children: "DitDev"
                    }), (0,
                    n.jsx)("meta", {
                        name: "description",
                        content: "A simple search engine"
                    }), (0,
                    n.jsx)("link", {
                        rel: "icon",
                        href: "/favicon.ico"
                    })]
                }), (0,
                n.jsxs)("main", {
                    "data-theme": e ? "dark" : "light",
                    className: "min-w-screen min-h-screen overflow-hidden",
                    children: [(0,
                    n.jsx)(o, {
                        post: t,
                        setPost: a,
                        toggle: l,
                        isDark: e
                    }), (0,
                    n.jsx)(d, {
                        post: t
                    })]
                })]
            })
        }
        ;
        var p = m
    }
}, function(e) {
    e.O(0, [636, 230, 774, 888, 179], function() {
        return e(e.s = 4182)
    }),
    _N_E = e.O()
}
]);
