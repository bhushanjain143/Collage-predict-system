// ---------- CONSTANTS ----------
const TOTAL_CANDIDATES = 410377; // MHT-CET 2024 PCM registered candidates (official CET Cell data)

// ---------- COLLEGE WEBSITE URLs ----------
// Uses KEYWORD-based matching — no need for exact name.
// Each entry: { keywords: [...], url: '...' }
// A college name matches if it contains ALL keywords (case-insensitive).
// Keywords should be unique enough to avoid wrong matches.
// For any college with no match, Google search is used as fallback automatically.
// ============================================================
//  COLLEGE URL MAP  —  100 TOP MAHARASHTRA ENGINEERING COLLEGES
//  Organised by city.  Each entry = college name keyword + official website.
//  To ADD a college:  copy any line, change name & URL, save file.
// ============================================================
const COLLEGE_URL_MAP = [

    // ════════════════════════════════════════════════════════════════
    //  NANDURBAR 
    //  1. COE Shahada              https://coeshahada.ac.in
    //  2. R.C. Patel, Shirpur      https://rcpit.ac.in
    //  3. North Maharashtra Univ   https://www.nmu.ac.in
    // ════════════════════════════════════════════════════════════════
    { keywords: ['D.N. Patel', 'Shahada'],           url: 'https://coeshahada.ac.in' },
    { keywords: ['D. N. Patel', 'Shahada'],          url: 'https://coeshahada.ac.in' },
    { keywords: ['DN Patel', 'Shahada'],             url: 'https://coeshahada.ac.in' },
    { keywords: ['R.C. Patel', 'Shirpur'],           url: 'https://rcpit.ac.in' },
    { keywords: ['RC Patel', 'Shirpur'],             url: 'https://rcpit.ac.in' },
    { keywords: ['North Maharashtra University'],    url: 'https://www.nmu.ac.in' },
    { keywords: ['MKD Institute of Technology'],     url: 'https://mkdit.edu.in' },
    { keywords: ['P.G. College', 'Nandurbar'],       url: 'https://pgcet.ac.in' },
    { keywords: ['PG College', 'Nandurbar'],         url: 'https://pgcet.ac.in' },
    // ════════════════════════════════════════════════════════════════
    //  MUMBAI  —  Government
    //  4.  VJTI Mumbai             https://vjti.ac.in
    //  5.  ICT Mumbai              https://ictmumbai.edu.in
    //  6.  Sardar Patel CE Andheri https://spce.ac.in
    // ════════════════════════════════════════════════════════════════
    { keywords: ['Veermata Jijabai'],                url: 'https://vjti.ac.in' },
    { keywords: ['VJTI'],                            url: 'https://vjti.ac.in' },
    { keywords: ['Institute of Chemical Technology','Mumbai'], url: 'https://ictmumbai.edu.in' },
    { keywords: ['Sardar Patel College of Engineering','Andheri'], url: 'https://spce.ac.in' },

    // ════════════════════════════════════════════════════════════════
    //  MUMBAI  —  Private / Autonomous
    //  7.  Thadomal Shahani (TSEC) https://tsec.edu
    //  8.  Fr. CRCE                https://frcrce.ac.in
    //  9.  VESIT                   https://vesit.ves.ac.in
    //  10. SAKEC                   https://sakec.ac.in
    //  11. KJ Somaiya              https://kjsieit.somaiya.edu
    //  12. Rizvi COE               https://rizvi.edu.in
    //  13. SPIT (Bhavan's)         https://spit.ac.in
    //  14. DJ Sanghvi              https://djsce.ac.in
    //  15. Vidyalankar IT          https://vit.edu.in
    //  16. Don Bosco IT            https://dbit.in
    //  17. St. Francis IT          https://sfit.ac.in
    //  18. Thakur CE (TCET)        https://tcetmumbai.in
    //  19. Atharva CE              https://atharvaengg.ac.in
    //  20. RGIT Mumbai             https://rgit.ac.in
    //  21. LTCE                    https://ltce.in
    //  22. Watumull                https://wieect.in
    // ════════════════════════════════════════════════════════════════
    { keywords: ['Thadomal Shahani'],                url: 'https://tsec.edu' },
    { keywords: ['TSEC'],                            url: 'https://tsec.edu' },
    { keywords: ['Fr. Conceicao Rodrigues'],         url: 'https://frcrce.ac.in' },
    { keywords: ['FRCRCE'],                          url: 'https://frcrce.ac.in' },
    { keywords: ['Vivekanand Education Society','Technology'], url: 'https://vesit.ves.ac.in' },
    { keywords: ['VESIT'],                           url: 'https://vesit.ves.ac.in' },
    { keywords: ['Shah & Anchor Kutchhi'],           url: 'https://sakec.ac.in' },
    { keywords: ['SAKEC'],                           url: 'https://sakec.ac.in' },
    { keywords: ['K J Somaiya'],                     url: 'https://kjsieit.somaiya.edu' },
    { keywords: ['KJ Somaiya'],                      url: 'https://kjsieit.somaiya.edu' },
    { keywords: ['Rizvi College of Engineering'],    url: 'https://rizvi.edu.in' },
    { keywords: ['Bhavan\'s Sardar Patel Institute','Andheri'], url: 'https://spit.ac.in' },
    { keywords: ['S.P.I.T'],                         url: 'https://spit.ac.in' },
    { keywords: ['Dwarkadas J. Sanghvi'],            url: 'https://djsce.ac.in' },
    { keywords: ['DJ Sanghvi'],                      url: 'https://djsce.ac.in' },
    { keywords: ['D.J. Sanghvi'],                    url: 'https://djsce.ac.in' },
    { keywords: ['Vidyalankar Institute of Technology'], url: 'https://vit.edu.in' },
    { keywords: ['Don Bosco Institute of Technology'], url: 'https://dbit.in' },
    { keywords: ['St. Francis Institute of Technology'], url: 'https://sfit.ac.in' },
    { keywords: ['SFIT'],                            url: 'https://sfit.ac.in' },
    { keywords: ['Thakur College of Engineering'],   url: 'https://tcetmumbai.in' },
    { keywords: ['TCET'],                            url: 'https://tcetmumbai.in' },
    { keywords: ['Atharva College of Engineering'],  url: 'https://atharvaengg.ac.in' },
    { keywords: ['Rajiv Gandhi Institute of Technology','Mumbai'], url: 'https://rgit.ac.in' },
    { keywords: ['RGIT','Mumbai'],                   url: 'https://rgit.ac.in' },
    { keywords: ['Lokmanya Tilak College'],          url: 'https://ltce.in' },
    { keywords: ['LTCE'],                            url: 'https://ltce.in' },
    { keywords: ['Watumull Institute'],              url: 'https://wieect.in' },

    // ════════════════════════════════════════════════════════════════
    //  NAVI MUMBAI
    //  23. Terna Engineering        https://ternaengg.ac.in
    //  24. Pillai COE               https://pce.ac.in
    //  25. Bharati Vidyapeeth Belapur https://bvcoenm.edu.in
    // ════════════════════════════════════════════════════════════════
    { keywords: ['Terna Engineering College'],       url: 'https://ternaengg.ac.in' },
    { keywords: ['Pillai College of Engineering'],   url: 'https://pce.ac.in' },
    { keywords: ['Bharati Vidyapeeth','Belapur'],    url: 'https://bvcoenm.edu.in' },

    // ════════════════════════════════════════════════════════════════
    //  THANE
    //  26. Vidyavardhini Vasai (VCET) https://vcet.ac.in
    //  27. Shree L.R. Tiwari (SLRTCE) https://slrtce.in
    //  28. Pravin Rohidas Patil       https://prpce.ac.in
    //  29. Yadavrao Tasgaonkar        https://ytcem.ac.in
    // ════════════════════════════════════════════════════════════════
    { keywords: ['Vidyavardhini','Vasai'],            url: 'https://vcet.ac.in' },
    { keywords: ['Shree L. R. Tiwari'],               url: 'https://slrtce.in' },
    { keywords: ['SLRTCE'],                           url: 'https://slrtce.in' },
    { keywords: ['Pravin Rohidas Patil'],             url: 'https://prpce.ac.in' },
    { keywords: ['Yadavrao Tasgaonkar'],              url: 'https://ytcem.ac.in' },

    // ════════════════════════════════════════════════════════════════
    //  PUNE  —  Government / Autonomous
    //  30. COEP Technological Univ    https://www.coeptech.ac.in
    //  31. GCE Karad                  https://gcekarad.ac.in
    //  32. Army Institute (AIT)       https://aitpune.edu.in
    // ════════════════════════════════════════════════════════════════
    { keywords: ['COEP Technological University'],   url: 'https://www.coeptech.ac.in' },
    { keywords: ['College of Engineering','Pune'],   url: 'https://www.coeptech.ac.in' },
    { keywords: ['Government College of Engineering','Karad'], url: 'https://gcekarad.ac.in' },
    { keywords: ['Army Institute of Technology'],    url: 'https://aitpune.edu.in' },
    { keywords: ['AIT','Pune'],                      url: 'https://aitpune.edu.in' },

    // ════════════════════════════════════════════════════════════════
    //  PUNE  —  Top Private / Autonomous
    //  33. PICT                        https://www.pict.edu
    //  34. VIT Pune                    https://www.vit.edu
    //  35. VIIT                        https://viit.ac.in
    //  36. SIT Symbiosis               https://www.sitpune.edu.in
    //  37. MITCOE                      https://mitcoe.edu.in
    //  38. MIT World Peace (MITWPU)    https://mitwpu.edu.in
    //  39. PCCOE                       https://www.pccoepune.com
    //  40. Bharati Vidyapeeth Pune     https://bvcoepune.edu.in
    //  41. PVG COE                     https://www.pvgcoet.ac.in
    //  42. Smt. Kashibai Navale (SKN)  https://www.skncoepune.ac.in
    //  43. MMCOE                       https://mmcoe.edu.in
    //  44. Sinhgad group               https://www.sinhgad.edu
    //  45. Cummins College             https://www.cumminscollege.in
    //  46. Indira COE (ICEM)           https://icem.ac.in
    //  47. Genba Sopanrao Moze         https://gsmcoe.ac.in
    //  48. Zeal COE                    https://zealcoe.com
    //  49. Flora IT                    https://floraengg.ac.in
    //  50. Alard COE                   https://alardcoe.ac.in
    //  51. DY Patil IT Pune            https://dypit.ac.in
    //  52. Navsahyadri                 https://navsahyadri.edu.in
    //  53. ISBM COE                    https://isbmcoe.org
    //  54. Samarth COE                 https://samarthengg.com
    //  55. Shree Ramchandra            https://www.srespune.org
    //  56. ISQUAREIT                   https://isquareit.edu.in
    //  57. Padmashri VB Kolte          https://pbkcoe.org
    // ════════════════════════════════════════════════════════════════
    { keywords: ['Pune Institute of Computer Technology'], url: 'https://www.pict.edu' },
    { keywords: ['PICT'],                            url: 'https://www.pict.edu' },
    { keywords: ['Vishwakarma Institute of Technology','Pune'], url: 'https://www.vit.edu' },
    { keywords: ['VIT','Pune'],                      url: 'https://www.vit.edu' },
    { keywords: ['Vishwakarma Institute of Information Technology'], url: 'https://viit.ac.in' },
    { keywords: ['VIIT'],                            url: 'https://viit.ac.in' },
    { keywords: ['Symbiosis Institute of Technology'], url: 'https://www.sitpune.edu.in' },
    { keywords: ['SIT','Symbiosis'],                 url: 'https://www.sitpune.edu.in' },
    { keywords: ['MIT College of Engineering','Kothrud'], url: 'https://mitcoe.edu.in' },
    { keywords: ['MITCOE'],                          url: 'https://mitcoe.edu.in' },
    { keywords: ['Dr. Vishwanath Karad MIT World Peace'], url: 'https://mitwpu.edu.in' },
    { keywords: ['MIT World Peace'],                 url: 'https://mitwpu.edu.in' },
    { keywords: ['Pimpri Chinchwad College of Engineering'], url: 'https://www.pccoepune.com' },
    { keywords: ['PCCOE'],                           url: 'https://www.pccoepune.com' },
    { keywords: ['Bharati Vidyapeeth College of Engineering','Dhankawadi'], url: 'https://bvcoepune.edu.in' },
    { keywords: ['BVCOEP'],                          url: 'https://bvcoepune.edu.in' },
    { keywords: ['PVG\'s College of Engineering'],   url: 'https://www.pvgcoet.ac.in' },
    { keywords: ['Pune Vidyarthi Griha'],            url: 'https://www.pvgcoet.ac.in' },
    { keywords: ['Smt. Kashibai Navale'],            url: 'https://www.skncoepune.ac.in' },
    { keywords: ['SKN','Sinhgad'],                   url: 'https://www.skncoepune.ac.in' },
    { keywords: ['Marathwada Mitra Mandal','College of Engineering'], url: 'https://mmcoe.edu.in' },
    { keywords: ['MMCOE'],                           url: 'https://mmcoe.edu.in' },
    { keywords: ['Sinhgad College of Engineering','Vadgaon'], url: 'https://www.sinhgad.edu' },
    { keywords: ['Sinhgad Institute of Technology'], url: 'https://www.sinhgad.edu' },
    { keywords: ['NBN Sinhgad'],                     url: 'https://www.sinhgad.edu' },
    { keywords: ['Cummins College'],                 url: 'https://www.cumminscollege.in' },
    { keywords: ['Indira College of Engineering'],   url: 'https://icem.ac.in' },
    { keywords: ['ICEM'],                            url: 'https://icem.ac.in' },
    { keywords: ['Genba Sopanrao Moze'],             url: 'https://gsmcoe.ac.in' },
    { keywords: ['Zeal College of Engineering'],     url: 'https://zealcoe.com' },
    { keywords: ['Flora Institute of Technology'],   url: 'https://floraengg.ac.in' },
    { keywords: ['Alard College'],                   url: 'https://alardcoe.ac.in' },
    { keywords: ['Dr. D.Y. Patil Institute of Technology','Pune'], url: 'https://dypit.ac.in' },
    { keywords: ['DY Patil Institute','Pune'],       url: 'https://dypit.ac.in' },
    { keywords: ['Navsahyadri'],                     url: 'https://navsahyadri.edu.in' },
    { keywords: ['ISBM College'],                    url: 'https://isbmcoe.org' },
    { keywords: ['Samarth College of Engineering'],  url: 'https://samarthengg.com' },
    { keywords: ['Shree Ramchandra College'],        url: 'https://www.srespune.org' },
    { keywords: ['International Institute of Information Technology','Pune'], url: 'https://isquareit.edu.in' },
    { keywords: ['Padmashri Dr. V.B. Kolte'],        url: 'https://pbkcoe.org' },

    // ════════════════════════════════════════════════════════════════
    //  NASHIK
    //  58. KK Wagh                     https://www.kkwagh.edu.in
    //  59. Sandip Institute            https://sandipinstitute.ac.in
    //  60. Amrutvahini COE             https://acoe.org.in
    //  61. Matoshri COE                https://mcoe.org
    //  62. Pravara Rural Engineering   https://prec.ac.in
    //  63. MET Bhujbal, Nashik         https://metbhujbal.edu.in
    //  64. GCE Nashik (Government)     https://gcenashik.ac.in
    // ════════════════════════════════════════════════════════════════
    { keywords: ['K.K. Wagh'],                       url: 'https://www.kkwagh.edu.in' },
    { keywords: ['KK Wagh'],                         url: 'https://www.kkwagh.edu.in' },
    { keywords: ['Sandip Institute of Technology'],  url: 'https://sandipinstitute.ac.in' },
    { keywords: ['Amrutvahini College'],             url: 'https://acoe.org.in' },
    { keywords: ['Matoshri College of Engineering'], url: 'https://mcoe.org' },
    { keywords: ['Pravara Rural Engineering'],       url: 'https://prec.ac.in' },
    { keywords: ['MET\'s Institute of Engineering','Nashik'], url: 'https://metbhujbal.edu.in' },
    { keywords: ['Government College of Engineering','Nashik'], url: 'https://gcenashik.ac.in' },

    // ════════════════════════════════════════════════════════════════
    //  NAGPUR
    //  65. VNIT Nagpur                 https://vnit.ac.in
    //  66. GCE Nagpur (Government)     https://gcoen.ac.in
    //  67. GH Raisoni COE              https://raisoni.net
    //  68. Ramdeobaba (RKNEC)          https://rknec.edu
    //  69. YCCE                        https://ycce.edu
    //  70. KDK College                 https://kdkce.edu.in
    //  71. Priyadarshini COE           https://pcenagpur.edu.in
    //  72. Tulsiramji Gaikwad (TGPCET) https://tgpcet.com
    //  73. Laxminarayan IT             https://lit.org.in
    //  74. Nagpur Institute of Tech    https://nitnapur.ac.in
    // ════════════════════════════════════════════════════════════════
    { keywords: ['Visvesvaraya National Institute'],  url: 'https://vnit.ac.in' },
    { keywords: ['VNIT'],                             url: 'https://vnit.ac.in' },
    { keywords: ['Government College of Engineering','Nagpur'], url: 'https://gcoen.ac.in' },
    { keywords: ['G.H. Raisoni College'],             url: 'https://raisoni.net' },
    { keywords: ['GH Raisoni'],                       url: 'https://raisoni.net' },
    { keywords: ['Ramdeobaba'],                       url: 'https://rknec.edu' },
    { keywords: ['Shri Ramdeobaba'],                  url: 'https://rknec.edu' },
    { keywords: ['RKNEC'],                            url: 'https://rknec.edu' },
    { keywords: ['Yeshwantrao Chavan College of Engineering'], url: 'https://ycce.edu' },
    { keywords: ['YCCE'],                             url: 'https://ycce.edu' },
    { keywords: ['K.D.K. College'],                   url: 'https://kdkce.edu.in' },
    { keywords: ['KDK College'],                      url: 'https://kdkce.edu.in' },
    { keywords: ['Priyadarshini College of Engineering'], url: 'https://pcenagpur.edu.in' },
    { keywords: ['Tulsiramji Gaikwad-Patil'],          url: 'https://tgpcet.com' },
    { keywords: ['TGPCET'],                            url: 'https://tgpcet.com' },
    { keywords: ['Laxminarayan Institute of Technology'], url: 'https://lit.org.in' },
    { keywords: ['Nagpur Institute of Technology'],   url: 'https://nitnapur.ac.in' },

    // ════════════════════════════════════════════════════════════════
    //  AURANGABAD / CHHATRAPATI SAMBHAJINAGAR
    //  75. GCE Aurangabad (Government)  https://geca.ac.in
    //  76. MGM COE                      https://mgmcoe.com
    //  77. Deogiri Institute            https://diemsaurangabad.ac.in
    //  78. MIT COE Aurangabad           https://mitcoeaurangabad.edu.in
    //  79. ICEEM                        https://iceem.in
    //  80. Marathwada IT (MIT)          https://mitaurangabad.edu.in
    // ════════════════════════════════════════════════════════════════
    { keywords: ['Government College of Engineering','Aurangabad'], url: 'https://geca.ac.in' },
    { keywords: ['MGM\'s College of Engineering'],    url: 'https://mgmcoe.com' },
    { keywords: ['Deogiri Institute'],                url: 'https://diemsaurangabad.ac.in' },
    { keywords: ['MIT College of Engineering','Aurangabad'], url: 'https://mitcoeaurangabad.edu.in' },
    { keywords: ['ICEEM'],                            url: 'https://iceem.in' },
    { keywords: ['International Centre Of Excellence','Engineering'], url: 'https://iceem.in' },
    { keywords: ['Marathwada Institute of Technology'], url: 'https://mitaurangabad.edu.in' },

    // ════════════════════════════════════════════════════════════════
    //  AMRAVATI
    //  81. GCE Amravati (Government)   https://gcoea.ac.in
    //  82. Sipna COE                   https://sipna.edu.in
    //  83. Shri Sant Gajanan Maharaj   https://ssgmce.ac.in
    //  84. PR Pote Patil               https://prpotepatilcoe.ac.in
    // ════════════════════════════════════════════════════════════════
    { keywords: ['Government College of Engineering','Amravati'], url: 'https://gcoea.ac.in' },
    { keywords: ['Sipna College'],                    url: 'https://sipna.edu.in' },
    { keywords: ['Shri Sant Gajanan Maharaj College'], url: 'https://ssgmce.ac.in' },
    { keywords: ['P. R. Pote Patil'],                 url: 'https://prpotepatilcoe.ac.in' },
    { keywords: ['PR Pote Patil'],                    url: 'https://prpotepatilcoe.ac.in' },

    // ════════════════════════════════════════════════════════════════
    //  KOLHAPUR
    //  85. GCE Kolhapur (Government)   https://gcekop.ac.in
    //  86. DY Patil COE, Kasba Bawada  https://dypct.ac.in
    //  87. KIT's COE Kolhapur          https://kitsce.edu.in
    //  88. Sanjay Ghodawat Institute   https://sgikolhapur.ac.in
    //  89. Sanjeevan Group             https://sanjeevanengg.ac.in
    //  90. Rajarambapu IT (RIT Sangli) https://ritindia.edu
    //  91. Tatyasaheb Kore IT (TKIET)  https://tkiet.ac.in
    // ════════════════════════════════════════════════════════════════
    { keywords: ['Government College of Engineering','Kolhapur'], url: 'https://gcekop.ac.in' },
    { keywords: ['D.Y.Patil College','Kasba Bawada'], url: 'https://dypct.ac.in' },
    { keywords: ['D Y Patil','Kasba Bawada'],         url: 'https://dypct.ac.in' },
    { keywords: ['KIT\'s College of Engineering','Kolhapur'], url: 'https://kitsce.edu.in' },
    { keywords: ['Sanjay Ghodawat'],                  url: 'https://sgikolhapur.ac.in' },
    { keywords: ['Sanjeevan Group'],                  url: 'https://sanjeevanengg.ac.in' },
    { keywords: ['Rajarambapu Institute of Technology'], url: 'https://ritindia.edu' },
    { keywords: ['RIT','Sangli'],                     url: 'https://ritindia.edu' },
    { keywords: ['Tatyasaheb Kore Institute'],        url: 'https://tkiet.ac.in' },
    { keywords: ['TKIET'],                            url: 'https://tkiet.ac.in' },

    // ════════════════════════════════════════════════════════════════
    //  SOLAPUR / NANDED / LATUR
    //  92. Walchand COE Sangli         https://walchandsangli.ac.in
    //  93. Karmayogi IT Solapur        https://kitsolapur.ac.in
    //  94. Shree Siddheshwar Women     https://sswcoe.edu.in
    //  95. GCE Latur (Government)      https://gcelatur.ac.in
    //  96. SGGS Nanded                 https://sggs.ac.in
    //  97. GRAMIN Technical Nanded     https://gtmc.edu.in
    // ════════════════════════════════════════════════════════════════
    { keywords: ['Walchand College of Engineering'],  url: 'https://walchandsangli.ac.in' },
    { keywords: ['Karmayogi Institute'],              url: 'https://kitsolapur.ac.in' },
    { keywords: ['Shree Siddheshwar Women'],          url: 'https://sswcoe.edu.in' },
    { keywords: ['Government College of Engineering','Latur'], url: 'https://gcelatur.ac.in' },
    { keywords: ['Shri Guru Gobind Singhji'],         url: 'https://sggs.ac.in' },
    { keywords: ['SGGS'],                             url: 'https://sggs.ac.in' },
    { keywords: ['GRAMIN TECHNICAL','NANDED'],        url: 'https://gtmc.edu.in' },

    // ════════════════════════════════════════════════════════════════
    //  DHULE / JALGAON / RATNAGIRI / OTHER
    //  98.  BS Deore COE Dhule         https://bsdeore.ac.in
    //  99.  GCE Jalgaon (Government)   https://gcejalgaon.ac.in
    //  100. Rajendra Mane COE Ratnagiri https://rmcet.com
    // ════════════════════════════════════════════════════════════════
    { keywords: ['B.S. Deore College'],              url: 'https://bsdeore.ac.in' },
    { keywords: ['S.S.V.P.S','Deore'],               url: 'https://bsdeore.ac.in' },
    { keywords: ['Government College of Engineering','Jalgaon'], url: 'https://gcejalgaon.ac.in' },
    { keywords: ['Rajendra Mane College'],           url: 'https://rmcet.com' },

];

// Smart lookup: finds URL by checking if college name contains ALL keywords (case-insensitive)
function getCollegeUrl(name) {
    var nameLower = (name || '').toLowerCase();
    for (var i = 0; i < COLLEGE_URL_MAP.length; i++) {
        var entry = COLLEGE_URL_MAP[i];
        var allMatch = entry.keywords.every(function(kw) {
            return nameLower.indexOf(kw.toLowerCase()) !== -1;
        });
        if (allMatch) return entry.url;
    }
    // Fallback: Google "I'm Feeling Lucky" — opens most relevant result directly
    // instead of showing a search results page
    return 'https://www.google.com/search?btnI=1&q=' + encodeURIComponent(name + ' official site Maharashtra engineering college');
}

// ---------- SIMPLE AUTH STATE ----------
const AUTH_REQUIRED_PAGES = [
    'dashboard'
];

function isUserLoggedIn() {
    return localStorage.getItem('explainai_user_logged_in') === 'true';
}

function setUserLoggedIn(value) {
    localStorage.setItem('explainai_user_logged_in', value ? 'true' : 'false');
}

function setCurrentUser(user) {
    try {
        localStorage.setItem('explainai_user', JSON.stringify(user || {}));
    } catch (e) {
        // ignore
    }
}

function getCurrentUser() {
    try {
        return JSON.parse(localStorage.getItem('explainai_user') || '{}');
    } catch (e) {
        return {};
    }
}

function refreshDashboardName() {
    const user = getCurrentUser();
    const name = (user && user.name) ? String(user.name).trim() : '';
    const displayName = name || 'Student';

    // Update all name elements
    ['dashName', 'dashName2'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = displayName;
    });

    // Update avatar letters
    ['dashAvatar', 'dashAvatar2'].forEach(id => {
        const av = document.getElementById(id);
        if (av) av.textContent = displayName.charAt(0).toUpperCase();
    });

    // Update days to CAP round 
    const daysEl = document.getElementById('dashDaysLeft');
    if (daysEl) {
        const target = new Date('2026-10-01');
        const now = new Date();
        const diff = Math.ceil((target - now) / (1000 * 60 * 60 * 24));
        daysEl.textContent = diff > 0 ? diff : 'Soon';
    }

    // Update all stats and activity (per-user data)
    updateDashboardStats();
    loadSavedPredictionRuns();
}

function getPostLoginRedirect() {
    return sessionStorage.getItem('explainai_post_login_redirect') || 'home';
}

function setPostLoginRedirect(pageId) {
    sessionStorage.setItem('explainai_post_login_redirect', pageId);
}

/** Same host when Flask serves the UI; Live Server / file:// use local API. */
const API_BASE = (function () {
    var proto = window.location.protocol;
    var port = window.location.port;
    if (proto === 'file:' || port === '5500') {
        return 'http://127.0.0.1:5000';
    }
    return '';
})();

/** Filled from GET /api/config — ai_enabled, data_year, etc. */
var APP_SERVER_CONFIG = { ai_enabled: false, data_year: null, cutoff_rows_approx: 0 };

/** Dashboard Chart.js instance */
var _dashChart = null;

async function refreshAppServerConfig() {
    try {
        var res = await fetch(API_BASE + '/api/config', { credentials: 'omit' });
        if (!res.ok) return;
        var j = await res.json();
        if (j.status === 'success') {
            APP_SERVER_CONFIG.ai_enabled = !!j.ai_enabled;
            APP_SERVER_CONFIG.data_year = j.data_year;
            APP_SERVER_CONFIG.cutoff_rows_approx = j.cutoff_rows_approx;
        }
    } catch (e) {
        /* offline */
    }
}

function _stripMdBold(s) {
    return String(s || '').replace(/\*\*/g, '');
}

// ---------- SEO / DOCUMENT META (SPA) ----------
const PAGE_SEO = {
    home: {
        title: 'ExplainAI — MHT-CET College Predictor & Counselling',
        description: 'MHT-CET college predictor, CAP-style counselling prep, optional AI summaries, and scholarship hints for Maharashtra. Not affiliated with CET Cell.'
    },
    counseling: {
        title: 'College Counselor — ExplainAI',
        description: 'Enter your MHT-CET percentile, category, and preferences to explore cutoff-aligned engineering college options in Maharashtra.'
    },
    'results-counseling': {
        title: 'College Results — ExplainAI',
        description: 'Review your MHT-CET college list by chance level. Export to PDF and verify every detail on official CAP notices.'
    },
    scholarship: {
        title: 'Scholarship Finder — ExplainAI',
        description: 'Explore scholarship-style matches for Maharashtra and central schemes. Confirm eligibility on MahaDBT and NSP.'
    },
    'results-scholarship': {
        title: 'Scholarship Results — ExplainAI',
        description: 'Scholarship exploration results from ExplainAI. Always apply on the official portal before deadlines.'
    },
    login: {
        title: 'Sign In — ExplainAI',
        description: 'Sign in to ExplainAI to save colleges, scholarships, and access your dashboard.'
    },
    register: {
        title: 'Create Account — ExplainAI',
        description: 'Create an ExplainAI account for MHT-CET college and scholarship tools.'
    },
    'forgot-password': {
        title: 'Reset Password — ExplainAI',
        description: 'Reset your ExplainAI account password.'
    },
    dashboard: {
        title: 'Dashboard — ExplainAI',
        description: 'Your counselling dashboard: saved prediction runs, liked colleges, scholarships, and quick links to tools.'
    }
};

function updateSeoForPage(pageId) {
    const meta = PAGE_SEO[pageId] || PAGE_SEO.home;
    document.title = meta.title;
    const descEl = document.getElementById('meta-description');
    if (descEl) {
        descEl.setAttribute('content', meta.description);
    }
}

function initSeoFromLocation() {
    if (!window.location.protocol || window.location.protocol === 'file:') {
        return;
    }
    try {
        const root = new URL('./', window.location.href).href;
        const absCover = new URL('images/og-cover.svg', root).href;
        const og = document.querySelector('meta[property="og:image"]');
        const tw = document.querySelector('meta[name="twitter:image"]');
        if (og) {
            og.setAttribute('content', absCover);
        }
        if (tw) {
            tw.setAttribute('content', absCover);
        }
        const url = window.location.href.split('#')[0];
        let link = document.getElementById('canonical-url');
        if (!link) {
            link = document.createElement('link');
            link.id = 'canonical-url';
            link.rel = 'canonical';
            document.head.appendChild(link);
        }
        link.setAttribute('href', url);
    } catch (e) {
        /* ignore */
    }
}

var _jspdfLoadPromise = null;
function ensureJsPdfLoaded() {
    if (typeof window.jspdf !== 'undefined' && window.jspdf.jsPDF) {
        return Promise.resolve();
    }
    if (_jspdfLoadPromise) {
        return _jspdfLoadPromise;
    }
    _jspdfLoadPromise = new Promise(function(resolve, reject) {
        const s1 = document.createElement('script');
        s1.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
        s1.async = true;
        s1.crossOrigin = 'anonymous';
        s1.onload = function() {
            const s2 = document.createElement('script');
            s2.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js';
            s2.async = true;
            s2.crossOrigin = 'anonymous';
            s2.onload = function() {
                resolve();
            };
            s2.onerror = function() {
                reject(new Error('jspdf-autotable'));
            };
            document.head.appendChild(s2);
        };
        s1.onerror = function() {
            reject(new Error('jspdf'));
        };
        document.head.appendChild(s1);
    });
    return _jspdfLoadPromise;
}

// ---------- AUTH HEADERS HELPER ----------
// Sends X-User-Id header as fallback when file:// origin blocks session cookies
function _authHeaders() {
    var user = getCurrentUser();
    var headers = { 'Content-Type': 'application/json' };
    if (user && user.id) {
        headers['X-User-Id'] = String(user.id);
    }
    return headers;
}


function isValidEmail(identifier) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(identifier);
}

function isValidPhone(identifier) {
    const digits = String(identifier || '').replace(/\D/g, '');
    return digits.length >= 10 && digits.length <= 15;
}

function isValidIdentifier(identifier) {
    const v = String(identifier || '').trim();
    return isValidEmail(v) || isValidPhone(v);
}

// ---------- MODAL DATA (Why? explanations) ----------
const modals = {
    coep: {
        title: 'Why we recommend COEP Pune — CSE',
        subtitle: 'College of Engineering, Pune · Computer Engineering',
        reasons: [
            { icon: '📊', text: '<strong>Your percentile input  exceeds last year\'s cutoff (98.40)</strong> for the OPEN category by 0.10 percentile points — placing you comfortably above the closing rank.' },
            { icon: '📍', text: '<strong>Location match:</strong> COEP is located in Pune, which matches your city preference.' },
            { icon: '🏛️', text: '<strong>College type match:</strong> COEP is a Government Autonomous institution, which you selected as a preference.' },
            { icon: '💰', text: '<strong>Budget compatible:</strong> Annual fees of ₹1,20,000 are within your stated budget of ₹1,50,000.' },
            { icon: '⭐', text: '<strong>Consistently high placements:</strong> COEP CSE has 95%+ placement rate with top MNCs recruiting on campus.' },
        ]
    },
    vit: {
        title: 'Why we recommend VIT Pune — CSE',
        subtitle: 'Vishwakarma Institute of Technology · Computer Engineering',
        reasons: [
            {  text: '<strong>Your percentile (98.50) exceeds last year\'s cutoff (97.80)</strong> by a comfortable margin of 0.70 points — strong chance of admission.' },
            {  text: '<strong>Location match:</strong> VIT Pune is situated in Pune.' },
            {  text: '<strong>Government-Aided institution</strong> — matched to your preference for Government/Aided colleges.' },
            {  text: '<strong>Budget compatible:</strong> Annual fees of ₹1,10,000 are within your budget.' },
        ]
    },
    pict: {
        title: 'Why PICT Pune — IT is Medium Chance',
        subtitle: 'PICT — Pune Institute of Computer Technology · IT',
        reasons: [
            {  text: '<strong>Slightly above your percentile:</strong> Last year\'s OPEN cutoff was 98.65, which is 0.15 points above your score of 98.50. This is a borderline situation.' },
            {  text: '<strong>Location match:</strong> PICT is in Pune, matching your preference.' },
            {  text: '<strong>Our advice:</strong> Apply here but don\'t rely on it. Cutoffs can shift year-on-year by ±0.3 percentile points, so admission is possible but not guaranteed.' },
        ]
    },
    sit: {
        title: 'Why SIT Pune — CSE is Medium Chance',
        subtitle: 'Symbiosis Institute of Technology · Computer Science',
        reasons: [
            {  text: '<strong>Cutoff of 98.55</strong> is slightly above your 98.50 — a gap of 0.05 points. Very close call.' },
            { text: '<strong>Budget caution:</strong> Annual fees of ₹2,40,000 exceed your stated budget of ₹1,50,000 by ₹90,000.' },
            {  text: 'If you apply here, explore SIT\'s merit scholarships which can offset the higher fee significantly.' },
        ]
    },
    vjti: {
        title: 'Why VJTI Mumbai — CSE is Low Chance / Risky',
        subtitle: 'Veermata Jijabai Technological Institute · Computer Engineering',
        reasons: [
            {  text: '<strong>Cutoff of 99.20 is significantly above your score of 98.50</strong> — a gap of 0.70 percentile points. Historical data shows this gap rarely closes year-on-year.' },
            {  text: '<strong>City mismatch:</strong> VJTI is in Mumbai, but you selected Pune as your preferred city.' },
            {  text: '<strong>Our advice:</strong> Include VJTI only if you\'re open to Mumbai and consider it a dream/reach college. Don\'t rely on it as a primary option.' },
        ]
    },
    scholarship1: {
        title: 'Why you\'re eligible for State Post-Matric (OBC)',
        subtitle: 'Maharashtra State Scholarship · MahaDBT Portal',
        reasons: [
            {  text: '<strong>Category match:</strong> This scholarship is for OBC students — you selected OBC category.' },
            {  text: '<strong>Income within limit:</strong> Your family income of ₹3.5L is well within the ₹8L annual income limit.' },
            {  text: '<strong>Domicile match:</strong> You are a Maharashtra domicile student, which is required.' },
            {  text: '<strong>Course eligible:</strong> Engineering (B.E.) is a covered course under this scholarship.' },
        ]
    },
    scholarship2: {
        title: 'Why you\'re eligible for CSSS',
        subtitle: 'Central Sector Scheme of Scholarships · NSP Portal',
        reasons: [
            {  text: '<strong>Merit criteria met:</strong> Your 12th grade score of 82% exceeds the 80% minimum required.' },
            {  text: '<strong>Income criteria:</strong> Family income below ₹4.5L qualifies for central scheme support.' },
            {  text: '<strong>First-generation benefit:</strong> You may be entitled to an additional supplement if no family member holds a degree.' },
        ]
    },
    scholarship3: {
        title: 'Why you\'re eligible for MahaDBT Maintenance Allowance',
        subtitle: 'Social Justice Dept., Maharashtra · MahaDBT',
        reasons: [
            {  text: '<strong>OBC category student</strong> pursuing higher education qualifies for maintenance support.' },
            {  text: '<strong>Maharashtra domicile</strong> — state-level support scheme.' },
            {  text: '<strong>Income below threshold</strong> — ₹3.5L is within the ₹6L OBC annual income limit.' },
        ]
    },
};

// ---------- PAGE NAVIGATION ----------
// Pages that need login — home page is always open to everyone
const PROTECTED_PAGES = ['dashboard', 'counseling', 'scholarship', 'results-counseling', 'results-scholarship'];

function showPage(id, force) {
    if (!force) {
        const loggedIn = localStorage.getItem('explainai_user_logged_in') === 'true';
        // Not logged in trying to access a protected page → remember destination, send to login
        if (PROTECTED_PAGES.includes(id) && !loggedIn) {
            setPostLoginRedirect(id);
            id = 'login';
        }
        // Already logged in → login/register pages redirect to home (not dashboard)
        if ((id === 'login' || id === 'register') && loggedIn) { id = 'home'; }
    }
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const page = document.getElementById('page-' + id);
    if (page) {
        page.classList.add('active');
        window.scrollTo(0, 0);
        updateSeoForPage(id);
        if (id === 'dashboard') { refreshDashboardName(); }
        if (id === 'results-counseling') { displayResultsMetadata(); }
        if (id === 'scholarship') { prefillScholarshipForm(); }

        // Auto-clear login/register form fields every time the page is shown
        if (id === 'login') {
            var lEmail  = document.getElementById('loginEmail');
            var lPass   = document.getElementById('loginPassword');
            var lErr    = document.getElementById('loginError');
            var lTerms  = document.getElementById('loginTerms');
            var lTermsErr = document.getElementById('loginTermsErr');
            if (lEmail)    lEmail.value   = '';
            if (lPass)     lPass.value    = '';
            if (lErr)      lErr.textContent = '';
            if (lTerms)    lTerms.checked = false;
            if (lTermsErr) lTermsErr.textContent = '';

            // Show green success banner after registration
            var regSuccess = sessionStorage.getItem('explainai_register_success');
            var successBanner = document.getElementById('loginSuccessBanner');
            if (regSuccess && successBanner) {
                successBanner.textContent = '\u2705 Account created! Welcome, ' + regSuccess + '. Please sign in below.';
                successBanner.style.display = 'block';
                sessionStorage.removeItem('explainai_register_success');
            } else if (successBanner) {
                successBanner.style.display = 'none';
            }

            // Show a helpful hint if user was redirected from a protected page
            var redirectDest = sessionStorage.getItem('explainai_post_login_redirect');
            var hintEl = document.getElementById('loginRedirectHint');
            var pageLabels = {
                'counseling': 'College Counselor',
                'scholarship': 'Scholarship Finder',
                'dashboard': 'your Dashboard',
                'results-counseling': 'College Results'
            };
            if (redirectDest && pageLabels[redirectDest] && hintEl) {
                hintEl.textContent = '\uD83D\uDD12 Sign in to access ' + pageLabels[redirectDest];
                hintEl.style.display = 'block';
            } else if (hintEl) {
                hintEl.style.display = 'none';
            }
        }
        if (id === 'register') {
            var rFields = ['regName','regEmail','regPassword','regConfirmPassword'];
            rFields.forEach(function(fid) {
                var el = document.getElementById(fid);
                if (el) el.value = '';
            });
            var rErr = page.querySelector('[id$="Error"]');
            if (rErr) rErr.textContent = '';
        }
    }
    updateNavBar();
    updateNavActive(id);
}

function updateNavActive(pageId) {
    document.querySelectorAll('.nav-links li a:not(.nav-cta)').forEach(a => {
        a.classList.remove('active');
        a.removeAttribute('aria-current');
    });
    document.querySelectorAll('.nav-links li a').forEach(a => {
        const onclick = a.getAttribute('onclick') || '';
        if (onclick.includes("'" + pageId + "'")) {
            a.classList.add('active');
            if (!a.classList.contains('nav-cta')) {
                a.setAttribute('aria-current', 'page');
            }
        }
    });
}

// ---------- PASSWORD VISIBILITY ----------
function togglePasswordVisibility(inputId, btn) {
    const input = document.getElementById(inputId);
    if (!input) return;
    const isPassword = input.type === 'password';
    input.type = isPassword ? 'text' : 'password';
    btn.textContent = isPassword ? 'Hide' : 'Show';
}

// ---------- LOGIN HANDLER ----------
function handleLogin(e) {
    e.preventDefault();
    const emailEl = document.getElementById('loginEmail');
    const passwordEl = document.getElementById('loginPassword');
    const errorDiv = document.getElementById('loginError');
    const emailErrEl = document.getElementById('loginEmailErr');
    const passwordErrEl = document.getElementById('loginPasswordErr');
    const btn = document.getElementById('loginSubmit');
    const termsEl    = document.getElementById('loginTerms');
    const termsErrEl = document.getElementById('loginTermsErr');

    // Clear errors
    [emailEl, passwordEl].forEach(i => i && i.classList.remove('input-error'));
    if (errorDiv)    errorDiv.textContent    = '';
    if (emailErrEl)  emailErrEl.textContent  = '';
    if (passwordErrEl) passwordErrEl.textContent = '';
    if (termsErrEl)  termsErrEl.textContent  = '';

    const emailVal = (emailEl?.value || '').trim();
    const passwordVal = (passwordEl?.value || '');

    // Client-side validation
    let hasErr = false;
    if (!isValidEmail(emailVal)) {
        emailEl.classList.add('input-error');
        if (emailErrEl) emailErrEl.textContent = 'Please enter a valid email address.';
        hasErr = true;
    }
    if (passwordVal.length < 1) {
        passwordEl.classList.add('input-error');
        if (passwordErrEl) passwordErrEl.textContent = 'Please enter your password.';
        hasErr = true;
    }
    if (termsEl && !termsEl.checked) {
        if (termsErrEl) termsErrEl.textContent = 'Please agree to the Terms & Conditions to continue.';
        hasErr = true;
    }
    if (hasErr) return;

    btn.disabled = true;
    btn.querySelector('span').textContent = 'Signing in...';

    (async () => {
        try {
            const res = await fetch(`${API_BASE}/api/auth/login`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ identifier: emailVal, password: passwordVal })
            });
            const result = await res.json();
            if (!res.ok || result.status !== 'success') {
                if (errorDiv) errorDiv.textContent = result.error || 'Login failed. Please try again.';
                return;
            }
            // Store user data from backend response
            const user = result.user || {};
            setUserLoggedIn(true);
            setCurrentUser({
                id: user.id,
                name: user.full_name || emailVal,
                email: user.email || emailVal,
                phone: user.phone || ''
            });
            const dest1 = getPostLoginRedirect() || 'home';
            sessionStorage.removeItem('explainai_post_login_redirect');
            showPage(dest1);
            updateSaveRunButtonVisibility();
        } catch (err) {
            // Backend not available — fallback for local dev (no DB)
            if (errorDiv) errorDiv.textContent = 'Cannot connect to server. Check that the backend is running.';
        } finally {
            btn.disabled = false;
            btn.querySelector('span').textContent = 'Sign In';
        }
    })();
}

// ---------- REGISTER HANDLER ----------
function handleRegister(e) {
    e.preventDefault();
    const nameEl    = document.getElementById('regName');
    const emailEl   = document.getElementById('regEmail');
    const phoneEl   = document.getElementById('regPhone');
    const passEl    = document.getElementById('regPassword');
    const confEl    = document.getElementById('regConfirmPassword');
    const errorDiv  = document.getElementById('registerError');
    const btn       = document.getElementById('registerSubmit');

    // Clear all errors
    [nameEl, emailEl, phoneEl, passEl, confEl].forEach(i => i && i.classList.remove('input-error'));
    ['regNameErr','regEmailErr','regPhoneErr','regPasswordErr','regConfirmErr'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = '';
    });
    if (errorDiv) errorDiv.textContent = '';

    const nameVal  = (nameEl?.value  || '').trim();
    const emailVal = (emailEl?.value || '').trim();
    const phoneVal = (phoneEl?.value || '').trim();
    const passVal  = passEl?.value || '';
    const confVal  = confEl?.value || '';
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^[0-9]{10}$/;

    let hasErr = false;
    function fieldError(el, errId, msg) {
        if (el) el.classList.add('input-error');
        const errEl = document.getElementById(errId);
        if (errEl) errEl.textContent = msg;
        if (!hasErr && el) el.focus();
        hasErr = true;
    }

    if (nameVal.length < 2)
        fieldError(nameEl, 'regNameErr', 'Please enter your full name (at least 2 characters).');
    if (!emailRegex.test(emailVal))
        fieldError(emailEl, 'regEmailErr', 'Please enter a valid email address.');
    if (phoneVal && !phoneRegex.test(phoneVal.replace(/\D/g,'')))
        fieldError(phoneEl, 'regPhoneErr', 'Enter a valid 10-digit phone number.');
    if (passVal.length < 8)
        fieldError(passEl, 'regPasswordErr', 'Password must be at least 8 characters.');
    else if (!/[A-Za-z]/.test(passVal) || !/[0-9]/.test(passVal))
        fieldError(passEl, 'regPasswordErr', 'Password must contain both letters and numbers.');
    if (passVal !== confVal)
        fieldError(confEl, 'regConfirmErr', 'Passwords do not match.');

    if (hasErr) return;

    btn.disabled = true;
    btn.querySelector('span').textContent = 'Creating account...';

    (async () => {
        try {
            const res = await fetch(`${API_BASE}/api/auth/register`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    full_name: nameVal,
                    email: emailVal,
                    phone: phoneVal,
                    password: passVal,
                    confirm_password: confVal
                })
            });
            const result = await res.json();
            if (!res.ok || result.status !== 'success') {
                // Field-level error from backend
                if (result.field) {
                    const fieldMap = {
                        full_name: 'regNameErr', email: 'regEmailErr',
                        phone: 'regPhoneErr', password: 'regPasswordErr',
                        confirm_password: 'regConfirmErr'
                    };
                    const errId = fieldMap[result.field];
                    if (errId) {
                        const errEl = document.getElementById(errId);
                        if (errEl) errEl.textContent = result.error;
                        const inputId = {regNameErr:'regName',regEmailErr:'regEmail',regPhoneErr:'regPhone',
                                         regPasswordErr:'regPassword',regConfirmErr:'regConfirmPassword'}[errId];
                        if (inputId) document.getElementById(inputId)?.classList.add('input-error');
                    } else {
                        if (errorDiv) errorDiv.textContent = result.error;
                    }
                } else {
                    if (errorDiv) errorDiv.textContent = result.error || 'Registration failed. Please try again.';
                }
                return;
            }
            // Success — redirect to login with success message
            sessionStorage.setItem('explainai_register_success', result.message || 'Registration successful. Please login to continue.');
            showPage('login', true);
        } catch (err) {
            if (errorDiv) errorDiv.textContent = 'Cannot connect to server. Check that the backend is running.';
        } finally {
            btn.disabled = false;
            btn.querySelector('span').textContent = 'Create  Account';
        }
    })();
}


// ---------- RESET PASSWORD HANDLER ----------
function handleResetPassword(e) {
    e.preventDefault();

    const emailEl    = document.getElementById('rpEmail');
    const newPassEl  = document.getElementById('rpNewPassword');
    const confPassEl = document.getElementById('rpConfirmPassword');
    const emailErr   = document.getElementById('rpEmailErr');
    const newPassErr = document.getElementById('rpNewPasswordErr');
    const confErr    = document.getElementById('rpConfirmPasswordErr');
    const errorDiv   = document.getElementById('rpError');
    const successDiv = document.getElementById('rpSuccessBanner');
    const notFound   = document.getElementById('rpNotFoundBanner');
    const btn        = document.getElementById('rpSubmitBtn');

    // Clear all previous messages
    [emailEl, newPassEl, confPassEl].forEach(el => el && el.classList.remove('input-error'));
    if (emailErr)   emailErr.textContent   = '';
    if (newPassErr) newPassErr.textContent = '';
    if (confErr)    confErr.textContent    = '';
    if (errorDiv)   errorDiv.textContent   = '';
    if (successDiv) successDiv.style.display = 'none';
    if (notFound)   notFound.style.display   = 'none';

    const emailVal   = (emailEl?.value   || '').trim();
    const newPassVal = (newPassEl?.value  || '');
    const confVal    = (confPassEl?.value || '');

    // Client-side validation
    let hasErr = false;
    if (!isValidEmail(emailVal)) {
        emailEl.classList.add('input-error');
        if (emailErr) emailErr.textContent = 'Please enter a valid email address.';
        hasErr = true;
    }
    if (newPassVal.length < 8) {
        newPassEl.classList.add('input-error');
        if (newPassErr) newPassErr.textContent = 'Password must be at least 8 characters.';
        hasErr = true;
    }
    if (confVal !== newPassVal) {
        confPassEl.classList.add('input-error');
        if (confErr) confErr.textContent = 'Passwords do not match.';
        hasErr = true;
    }
    if (hasErr) return;

    btn.disabled = true;
    btn.querySelector('span').textContent = 'Resetting...';

    (async () => {
        try {
            const res = await fetch(`${API_BASE}/api/auth/reset-password`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: emailVal, new_password: newPassVal })
            });
            const result = await res.json();

            if (res.status === 404 || result.error === 'user_not_found' || result.status === 'not_found') {
                if (notFound) notFound.style.display = 'block';
                return;
            }
            if (!res.ok || result.status !== 'success') {
                if (errorDiv) errorDiv.textContent = result.error || 'Reset failed. Please try again.';
                return;
            }
            // Success
            if (successDiv) {
                successDiv.textContent = ' Password reset successfully. Please login with your new password.';
                successDiv.style.display = 'block';
            }
            ['rpEmail','rpNewPassword','rpConfirmPassword'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.value = '';
            });
            setTimeout(() => { showPage('login', true); }, 2000);

        } catch (err) {
            if (errorDiv) errorDiv.textContent = 'Cannot connect to server. Please make sure the backend is running.';
        } finally {
            btn.disabled = false;
            btn.querySelector('span').textContent = 'Reset Password';
        }
    })();
}

// ---------- LOGOUT ----------
function logout() {
    // Clear ALL per-user scoped data for the current user before sign-out
    // This prevents the next user seeing previous user's saved colleges,
    // scholarships, activity, and stats on the same browser.
    var user = getCurrentUser();
    var uid  = (user && (user.id || user.email)) ? String(user.id || user.email) : null;
    if (uid) {
        var keySuffixes = [
            'explainai_liked', 'explainai_disliked', 'explainai_activity',
            'explainai_scholar_liked', 'explainai_scholar_disliked',
            'explainai_scholar_total', 'explainai_last_total'
        ];
        keySuffixes.forEach(function(base) {
            localStorage.removeItem(base + '_' + uid);
        });
    }
    // Clear auth state
    localStorage.removeItem('explainai_user_logged_in');
    localStorage.removeItem('explainai_user');
    sessionStorage.clear();
    // Also clear backend session
    fetch(`${API_BASE}/api/auth/logout`, {
        method: 'POST',
        credentials: 'include'
    }).catch(() => {});
    showPage('login', true);  // force=true bypasses login check
}

// ---------- NAVBAR UPDATE ----------
function handleNavAuth() {
    const loggedIn = localStorage.getItem('explainai_user_logged_in') === 'true';
    if (loggedIn) {
        logout();
    } else {
        showPage('login', true);
    }
}

function updateNavBar() {
    const loggedIn = localStorage.getItem('explainai_user_logged_in') === 'true';
    const btn = document.getElementById('navAuthBtn');
    if (btn) {
        btn.textContent = loggedIn ? 'Sign Out' : 'Sign In';
        btn.style.background = loggedIn ? '#fee2e2' : '';
        btn.style.color = loggedIn ? '#c53030' : '';
    }
}

// ---------- AUTH PASSWORD TOGGLE ----------
function toggleAuthPassword(inputId, btn) {
    const input = document.getElementById(inputId);
    if (!input) return;
    const img = btn.querySelector('.eye-icon');
    if (input.type === 'password') {
        input.type = 'text';
        if (img) img.src = 'images/eye-hide.svg';
        btn.setAttribute('aria-label', 'Hide password');
    } else {
        input.type = 'password';
        if (img) img.src = 'images/eye-show.svg';
        btn.setAttribute('aria-label', 'Show password');
    }
}

// ---------- CHIP TOGGLES ----------
function toggleChip(el) {
    el.classList.toggle('selected');
}

function filterActive(el) {
    document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
}

// ---------- LIKE / DISLIKE ----------
// User-scoped storage keys — prevents one user's data showing for another user
function _userStorageKey(base) {
    var user = getCurrentUser();
    var uid  = (user && (user.id || user.email)) ? String(user.id || user.email) : 'guest';
    return base + '_' + uid;
}

function _getLiked()    { try { return JSON.parse(localStorage.getItem(_userStorageKey('explainai_liked'))    || '[]'); } catch(e) { return []; } }
function _getDisliked() { try { return JSON.parse(localStorage.getItem(_userStorageKey('explainai_disliked')) || '[]'); } catch(e) { return []; } }
function _getActivity() { try { return JSON.parse(localStorage.getItem(_userStorageKey('explainai_activity')) || '[]'); } catch(e) { return []; } }

function _saveLiked(arr)    { localStorage.setItem(_userStorageKey('explainai_liked'),    JSON.stringify(arr)); }
function _saveDisliked(arr) { localStorage.setItem(_userStorageKey('explainai_disliked'), JSON.stringify(arr)); }

function _addActivity(text) {
    var arr = _getActivity();
    arr.unshift({ text: text, time: Date.now() });
    if (arr.length > 20) arr = arr.slice(0, 20);
    localStorage.setItem(_userStorageKey('explainai_activity'), JSON.stringify(arr));
}

function toggleLike(btn, collegeKey, collegeName, collegeBranch) {
    var liked    = _getLiked();
    var disliked = _getDisliked();
    var isLiked  = liked.includes(collegeKey);

    // Find the matching dislike button (sibling)
    var card       = btn.closest('.result-card');
    var dislikeBtn = card ? card.querySelector('.rc-dislike') : null;

    if (isLiked) {
        // ── UN-LIKE: remove from localStorage + remove from DB ──
        _saveLiked(liked.filter(function(k) { return k !== collegeKey; }));
        btn.classList.remove('active-like');

        // Remove like from backend database
        fetch(API_BASE + '/api/likes', {
            method: 'DELETE',
            credentials: 'include',
            headers: _authHeaders(),
            body: JSON.stringify({
                college_name: collegeName,
                branch:       collegeBranch || ''
            })
        }).catch(function(err) {
            console.warn('Unlike API error (non-critical):', err);
        });

    } else {
        // ── LIKE: save to localStorage + save to DB ──
        liked.push(collegeKey);
        _saveLiked(liked);
        _saveDisliked(disliked.filter(function(k) { return k !== collegeKey; }));
        btn.classList.add('active-like');
        if (dislikeBtn) dislikeBtn.classList.remove('active-dislike');
        _addActivity('Saved: ' + collegeName);

        // Save like to backend database
        fetch(API_BASE + '/api/likes', {
            method: 'POST',
            credentials: 'include',
            headers: _authHeaders(),
            body: JSON.stringify({
                college_name: collegeName,
                branch:       collegeBranch || ''
            })
        }).then(function(res) {
            return res.json();
        }).then(function(result) {
            if (result.status === 'success') {
                console.log('Like saved to database:', collegeName);
            } else if (result.status === 'already_liked') {
                console.log('Already liked in database:', collegeName);
            } else if (result.status === 'error' && result.error === 'Not logged in. Please sign in first.') {
                console.warn('Like not saved to DB — user not logged in (saved locally only)');
            }
        }).catch(function(err) {
            console.warn('Like API error (like saved locally only):', err);
        });
    }
    updateDashboardStats();
}

function toggleDislike(btn, collegeKey, collegeName, collegeBranch) {
    var liked    = _getLiked();
    var disliked = _getDisliked();
    var isDisliked = disliked.includes(collegeKey);

    var card      = btn.closest('.result-card');
    var likeBtn   = card ? card.querySelector('.rc-like') : null;

    if (isDisliked) {
        // ── UN-DISLIKE: remove from localStorage + remove from DB ──
        _saveDisliked(disliked.filter(function(k) { return k !== collegeKey; }));
        btn.classList.remove('active-dislike');

        // Remove dislike from backend database
        fetch(API_BASE + '/api/dislikes', {
            method: 'DELETE',
            credentials: 'include',
            headers: _authHeaders(),
            body: JSON.stringify({
                college_name: collegeName,
                branch:       collegeBranch || ''
            })
        }).catch(function(err) {
            console.warn('Un-dislike API error (non-critical):', err);
        });

    } else {
        // ── DISLIKE: save to localStorage + save to DB ──
        disliked.push(collegeKey);
        _saveDisliked(disliked);
        _saveLiked(liked.filter(function(k) { return k !== collegeKey; }));
        btn.classList.add('active-dislike');
        if (likeBtn) likeBtn.classList.remove('active-like');
        _addActivity('Not Interested: ' + collegeName);

        // Save dislike to backend database
        fetch(API_BASE + '/api/dislikes', {
            method: 'POST',
            credentials: 'include',
            headers: _authHeaders(),
            body: JSON.stringify({
                college_name: collegeName,
                branch:       collegeBranch || ''
            })
        }).then(function(res) {
            return res.json();
        }).then(function(result) {
            if (result.status === 'success') {
                console.log('Dislike saved to database:', collegeName);
            } else if (result.status === 'already_disliked') {
                console.log('Already disliked in database:', collegeName);
            } else if (result.status === 'error') {
                console.warn('Dislike not saved to DB:', result.error);
            }
        }).catch(function(err) {
            console.warn('Dislike API error (saved locally only):', err);
        });
    }
    updateDashboardStats();
}

// Keep toggleSave as alias for backward compat (used nowhere now, but safe)
function toggleSave(btn) { /* replaced by toggleLike/toggleDislike */ }

function updateDashSavedCount() { updateDashboardStats(); }

function initEaTheme() {
    var saved = localStorage.getItem('ea-bs-theme');
    var prefers = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    var mode = saved || (prefers ? 'dark' : 'light');
    applyEaTheme(mode);
    var btn = document.getElementById('themeToggle');
    if (btn) {
        btn.addEventListener('click', function () {
            var cur = document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'dark' : 'light';
            var next = cur === 'dark' ? 'light' : 'dark';
            applyEaTheme(next);
            try {
                localStorage.setItem('ea-bs-theme', next);
            } catch (e) { /* */ }
            if (typeof refreshDashChart === 'function') {
                refreshDashChart();
            }
        });
    }
}

function applyEaTheme(mode) {
    var dark = mode === 'dark';
    document.documentElement.setAttribute('data-bs-theme', dark ? 'dark' : 'light');
    var icon = document.getElementById('themeToggleIcon');
    if (icon) {
        icon.className = dark ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
    }
}

function _parseDashStat(elId) {
    var el = document.getElementById(elId);
    if (!el) return 0;
    var t = (el.textContent || '').trim();
    if (t === '' || t === '\u2014' || t === '—') return 0;
    var n = parseInt(t, 10);
    return isNaN(n) ? 0 : n;
}

function refreshDashChart() {
    var canvas = document.getElementById('dashStatsChart');
    if (!canvas || typeof Chart === 'undefined') return;
    var ctx = canvas.getContext('2d');
    if (!ctx) return;
    var labels = ['Saved runs', 'Colleges analysed', 'Colleges saved', 'Scholarships matched', 'Scholarships saved'];
    var data = [
        _parseDashStat('dashPredictionRunsCount'),
        _parseDashStat('dashAnalysedCount'),
        _parseDashStat('dashSavedCount'),
        _parseDashStat('dashScholarAnalysedCount'),
        _parseDashStat('dashScholarSavedCount')
    ];
    var isDark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
    var gridColor = isDark ? 'rgba(148,163,184,.22)' : 'rgba(15,23,42,.08)';
    var fontColor = isDark ? '#e2e8f0' : '#334155';
    if (_dashChart) {
        _dashChart.destroy();
        _dashChart = null;
    }
    _dashChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Activity',
                data: data,
                borderRadius: 8,
                backgroundColor: ['#6366f1', '#0ea5e9', '#22c55e', '#a855f7', '#f59e0b']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    ticks: { color: fontColor, maxRotation: 40, autoSkip: true, font: { size: 10 } },
                    grid: { color: gridColor }
                },
                y: {
                    beginAtZero: true,
                    ticks: { color: fontColor, precision: 0, font: { size: 10 } },
                    grid: { color: gridColor }
                }
            }
        }
    });
}

function updateDashboardStats() {
    var liked         = _getLiked();
    var disliked      = _getDisliked();
    var scholarLiked  = _getScholarLiked();
    var grid          = document.getElementById('resultsGrid');
    var total         = grid && grid._all ? grid._all.length : 0;

    // Stat cards
    var el;
    el = document.getElementById('dashSavedCount');       if (el) el.textContent = liked.length;
    el = document.getElementById('dashDislikedCount');    if (el) el.textContent = disliked.length;
    el = document.getElementById('dashAnalysedCount');    if (el) el.textContent = total > 0 ? total : (parseInt(localStorage.getItem(_userStorageKey('explainai_last_total')) || '0') || '—');

    // Scholarships Eligible — stored when scholarship results are rendered
    var scholarRaw   = localStorage.getItem(_userStorageKey('explainai_scholar_total'));
    var scholarTotal = scholarRaw !== null ? parseInt(scholarRaw) : '—';
    el = document.getElementById('dashScholarAnalysedCount'); if (el) el.textContent = scholarTotal;

    // Scholarships Saved — count of scholarships user has saved
    el = document.getElementById('dashScholarSavedCount'); if (el) el.textContent = scholarLiked.length;

    // Save last total so dashboard shows it even after navigation
    if (total > 0) localStorage.setItem(_userStorageKey('explainai_last_total'), total);

    // Render recent activity
    _renderActivity();
    refreshDashChart();
}

function _renderActivity() {
    var collegeList  = document.getElementById('dashCollegeActivityList');
    var scholarList  = document.getElementById('dashScholarActivityList');

    var activityLog = _getActivity(); // [{text, time}, ...]

    var collegeItems = [];
    var scholarItems = [];

    activityLog.forEach(function(entry) {
        var text = entry.text || '';
        if (text.indexOf('Saved scholarship:') === 0) {
            var name = text.replace('Saved scholarship:', '').trim();
            scholarItems.push({ text: name, sub: 'Scholarship Saved', color: 'dai-blue' });
        } else if (text.indexOf('Saved:') === 0) {
            var label = text.replace('Saved:', '').trim();
            collegeItems.push({ text: label, sub: 'College Saved', color: 'dai-green' });
        }
    });

    collegeItems = collegeItems.slice(0, 6);
    scholarItems = scholarItems.slice(0, 6);

    function _renderItems(items) {
        return items.map(function(it) {
            return '<div class="dash-activity-item ' + it.color + '">' +
                '<div class="dai-dot"></div>' +
                '<div class="dai-body">' +
                    '<div class="dai-name dai-name-wrap">' + it.text + '</div>' +
                    '<div class="dai-meta">' + it.sub + '</div>' +
                '</div>' +
            '</div>';
        }).join('');
    }

    if (collegeList) {
        collegeList.innerHTML = collegeItems.length > 0
            ? _renderItems(collegeItems)
            : '<div class="dai-empty">No colleges saved yet — start exploring!</div>';
    }

    if (scholarList) {
        scholarList.innerHTML = scholarItems.length > 0
            ? _renderItems(scholarItems)
            : '<div class="dai-empty">No scholarships saved yet — find scholarships!</div>';
    }
}

async function loadSavedPredictionRuns() {
    var listEl = document.getElementById('dashPredictionsList');
    var cntEl = document.getElementById('dashPredictionRunsCount');
    if (!listEl) return;
    if (!getCurrentUser() || !getCurrentUser().id) {
        listEl.innerHTML = '<div class="dai-empty">Sign in and use &quot;Save run&quot; on results to store a shortlist here.</div>';
        if (cntEl) cntEl.textContent = '0';
        refreshDashChart();
        return;
    }
    try {
        var res = await fetch(API_BASE + '/api/predictions', { credentials: 'include', headers: _authHeaders() });
        var data = await res.json();
        if (data.status !== 'success' || !data.predictions || !data.predictions.length) {
            listEl.innerHTML = '<div class="dai-empty">No saved runs yet — open results and click Save run.</div>';
            if (cntEl) cntEl.textContent = '0';
            refreshDashChart();
            return;
        }
        if (cntEl) cntEl.textContent = String(data.predictions.length);
        listEl.innerHTML = data.predictions.map(function (p) {
            var sub = (p.percentile != null ? 'Pct ' + p.percentile : '') +
                (p.category ? ' · ' + p.category : '') +
                (p.college_count != null ? ' · ' + p.college_count + ' colleges' : '');
            return '<div class="dash-activity-item dai-blue">' +
                '<div class="dai-dot"></div><div class="dai-body">' +
                '<div class="dai-name dai-name-wrap">' + (p.title || 'Run') + '</div>' +
                '<div class="dai-meta">' + (p.created_at || '') + (sub ? ' — ' + sub : '') + '</div>' +
                '</div></div>';
        }).join('');
    } catch (e) {
        listEl.innerHTML = '<div class="dai-empty">Could not load saved runs (is the backend running?).</div>';
        if (cntEl) cntEl.textContent = '—';
    }
    refreshDashChart();
}

function updateSaveRunButtonVisibility() {
    var saveBtn = document.getElementById('btnSavePredictionRun');
    if (!saveBtn) return;
    saveBtn.style.display = getCurrentUser() && getCurrentUser().id ? '' : 'none';
}

async function savePredictionRun() {
    var grid = document.getElementById('resultsGrid');
    if (!grid || !grid._all || !grid._all.length) {
        alert('No results to save.');
        return;
    }
    if (!getCurrentUser() || !getCurrentUser().id) {
        alert('Please sign in to save this prediction run to your account.');
        showPage('login');
        return;
    }
    var form = {
        percentile: parseFloat(sessionStorage.getItem('inputPercentile') || '0'),
        category: sessionStorage.getItem('inputCategory') || '',
        city: sessionStorage.getItem('inputCity') || ''
    };
    var title = 'Run · pct ' + form.percentile + ' · ' + (form.category || 'OPEN');
    try {
        var res = await fetch(API_BASE + '/api/predictions', {
            method: 'POST',
            credentials: 'include',
            headers: _authHeaders(),
            body: JSON.stringify({ title: title, form: form, colleges: grid._all })
        });
        var data = await res.json();
        if (data.status === 'success') {
            alert('Saved to your account. View it on the Dashboard.');
            loadSavedPredictionRuns();
        } else {
            alert(data.error || 'Could not save.');
        }
    } catch (e) {
        alert('Network error while saving.');
    }
}

async function requestAiInsight(task) {
    var grid = document.getElementById('resultsGrid');
    var panel = document.getElementById('aiInsightPanel');
    var meta = document.getElementById('aiInsightMeta');
    var txt = document.getElementById('aiInsightText');
    if (!grid || !panel || !txt) return;
    var colleges = grid._all || [];
    if (!colleges.length) {
        alert('No colleges to analyse.');
        return;
    }
    panel.style.display = 'block';
    meta.textContent = 'Generating…';
    txt.textContent = '';
    var body = {
        task: task === 'guidance' ? 'guidance' : 'explain_list',
        percentile: parseFloat(sessionStorage.getItem('inputPercentile') || '0'),
        category: sessionStorage.getItem('inputCategory') || '',
        city: sessionStorage.getItem('inputCity') || '',
        colleges: colleges.slice(0, 40).map(function (c) {
            return {
                college_name: c.college_name,
                branch: c.branch,
                chance: c.chance,
                cutoff_percentile: c.cutoff_percentile,
                city: c.city
            };
        })
    };
    try {
        var res = await fetch(API_BASE + '/api/ai/explain', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        var data = await res.json();
        var provider = data.provider ? ' · ' + data.provider : '';
        var st = data.status === 'ok' ? 'AI insight' : (data.status === 'disabled' ? 'Guidance (offline mode)' : 'Guidance');
        meta.textContent = st + provider;
        txt.textContent = data.text || data.error || 'No text returned.';
        try {
            sessionStorage.setItem('explainai_last_ai_summary', txt.textContent);
        } catch (e2) { /* quota */ }
    } catch (e) {
        meta.textContent = 'Error';
        txt.textContent = 'Could not reach the AI service. Check your connection and that the backend is running.';
    }
}

async function requestCardBatchInsights() {
    var grid = document.getElementById('resultsGrid');
    var panel = document.getElementById('aiInsightPanel');
    var meta = document.getElementById('aiInsightMeta');
    var txt = document.getElementById('aiInsightText');
    if (!grid || !panel || !txt) return;
    var colleges = grid._all || [];
    if (!colleges.length) {
        alert('No colleges to analyse.');
        return;
    }
    panel.style.display = 'block';
    meta.textContent = 'Generating per-college insights…';
    txt.textContent = '';
    var body = {
        percentile: parseFloat(sessionStorage.getItem('inputPercentile') || '0'),
        category: sessionStorage.getItem('inputCategory') || '',
        colleges: colleges.slice(0, 25).map(function (c) {
            return {
                college_name: c.college_name,
                branch: c.branch,
                chance: c.chance,
                cutoff_percentile: c.cutoff_percentile,
                city: c.city
            };
        })
    };
    try {
        var res = await fetch(API_BASE + '/api/ai/card-insights', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        var data = await res.json();
        var provider = data.provider ? ' · ' + data.provider : '';
        meta.textContent = (data.status === 'ok' ? 'Per-college insights' : 'Insights') + provider;
        txt.textContent = data.text || data.error || 'No text returned.';
        try {
            sessionStorage.setItem('explainai_last_ai_summary', txt.textContent);
        } catch (e2) { /* quota */ }
    } catch (e) {
        meta.textContent = 'Error';
        txt.textContent = 'Could not reach the AI service.';
    }
}

function _getCounselorHistory() {
    try {
        var raw = sessionStorage.getItem('explainai_counselor_history');
        var h = raw ? JSON.parse(raw) : [];
        return Array.isArray(h) ? h : [];
    } catch (e) {
        return [];
    }
}

function _appendCounselorTurn(role, content) {
    var h = _getCounselorHistory();
    h.push({ role: role, content: String(content || '') });
    if (h.length > 24) {
        h = h.slice(-24);
    }
    try {
        sessionStorage.setItem('explainai_counselor_history', JSON.stringify(h));
    } catch (e2) { /* quota */ }
}

function _renderCounselorMessages() {
    var box = document.getElementById('counselorMessages');
    if (!box) return;
    var h = _getCounselorHistory();
    if (!h.length) {
        box.innerHTML = '<div style="opacity:.85;font-size:12px">Your conversation will appear here. Try a quick button or type a question.</div>';
        return;
    }
    box.innerHTML = h.map(function (m) {
        var isUser = m.role === 'user';
        var bg = isUser ? 'rgba(255,255,255,.12)' : 'rgba(0,0,0,.12)';
        var lab = isUser ? 'You' : 'Counselor';
        var esc = String(m.content || '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\n/g, '<br/>');
        return '<div style="margin-bottom:10px;padding:8px 10px;border-radius:8px;background:' + bg + '">' +
            '<div style="font-size:10px;opacity:.75;margin-bottom:4px">' + lab + '</div>' +
            '<div style="font-size:13px">' + esc + '</div></div>';
    }).join('');
    box.scrollTop = box.scrollHeight;
}

function _counselorCollegePayload() {
    var grid = document.getElementById('resultsGrid');
    var colleges = (grid && grid._all) ? grid._all : [];
    return colleges.slice(0, 12).map(function (c) {
        return {
            college_name: c.college_name,
            branch: c.branch,
            chance: c.chance,
            cutoff_percentile: c.cutoff_percentile,
            city: c.city
        };
    });
}

async function sendCounselorChat() {
    var inp = document.getElementById('counselorInput');
    if (!inp) return;
    var q = (inp.value || '').trim();
    if (!q) return;
    inp.value = '';
    await _runCounselorQuestion(q);
}

async function sendCounselorQuick(kind) {
    var q = '';
    if (kind === 'best_choice') {
        q = 'In 5–8 lines, what is the single best choice for me from this list and why? End with whether the overall mix looks safe, moderate, or risky for CAP.';
    } else if (kind === 'compare_top2') {
        q = 'Compare only the first two colleges on my predicted list (by order shown). Cover placements (as trends, not exact numbers unless from data), branch value, location, and which option is relatively safer for me.';
    } else if (kind === 'next_steps') {
        q = 'What concrete CAP / counselling steps should I take in the next two weeks? Use a numbered list.';
    } else {
        return;
    }
    await _runCounselorQuestion(q);
}

async function _runCounselorQuestion(question) {
    if (!APP_SERVER_CONFIG.ai_enabled) {
        alert('AI is not configured on the server (add OPENAI_API_KEY or GEMINI_API_KEY).');
        return;
    }
    var grid = document.getElementById('resultsGrid');
    if (!grid || !grid._all || !grid._all.length) {
        alert('No college list loaded.');
        return;
    }
    var hist = _getCounselorHistory();
    var body = {
        question: question,
        percentile: parseFloat(sessionStorage.getItem('inputPercentile') || '0'),
        category: sessionStorage.getItem('inputCategory') || '',
        city: sessionStorage.getItem('inputCity') || '',
        colleges: _counselorCollegePayload(),
        history: hist
    };
    try {
        var res = await fetch(API_BASE + '/api/ai/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        var data = await res.json();
        var text = data.text || data.error || 'No reply.';
        _appendCounselorTurn('user', question);
        _appendCounselorTurn('assistant', text);
        _renderCounselorMessages();
    } catch (e) {
        alert('Could not reach the counselor API.');
    }
}

function openGenericAdviceModal(title, plainBody) {
    var kickerEl = document.getElementById('modal-kicker');
    if (kickerEl) kickerEl.textContent = 'AI guidance';
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-subtitle').textContent = 'Double-check every step on the official portal.';
    var wrap = document.getElementById('modal-reasons');
    wrap.innerHTML = '';
    var pre = document.createElement('pre');
    pre.style.whiteSpace = 'pre-wrap';
    pre.style.fontFamily = 'inherit';
    pre.style.fontSize = '13px';
    pre.style.lineHeight = '1.5';
    pre.style.margin = '0';
    pre.textContent = plainBody;
    wrap.appendChild(pre);
    document.getElementById('modal-overlay').classList.add('open');
}

async function requestScholarshipApplyGuide(scholarId) {
    if (!APP_SERVER_CONFIG.ai_enabled) {
        alert('AI is not configured on the server.');
        return;
    }
    var p = window._scholarApplyPayload && window._scholarApplyPayload[scholarId];
    if (!p) {
        alert('Scholarship data not found. Run the scholarship search again.');
        return;
    }
    try {
        var res = await fetch(API_BASE + '/api/ai/scholarship-guide', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: p.name,
                portal_url: p.portal_url,
                documents: p.documents || [],
                category: p.category || ''
            })
        });
        var data = await res.json();
        openGenericAdviceModal('How to apply: ' + (p.name || 'Scholarship'), data.text || data.error || 'No text.');
    } catch (e) {
        alert('Could not reach the AI service.');
    }
}


function openModal(key) {
    const m = modals[key];
    if (!m) return;
    var kicker = document.getElementById('modal-kicker');
    if (kicker) {
        kicker.textContent = m.chanceLevel ? 'Open breakdown — not a black box' : 'How we chose this';
    }
    document.getElementById('modal-title').textContent = m.title;
    document.getElementById('modal-subtitle').textContent = m.subtitle || '';

    var html = '';

    if (m.chanceLevel) {
        // Structured format for college result cards
        var chanceCls = m.chanceLevel.toLowerCase() === 'high'   ? 'why-chance-high'
                      : m.chanceLevel.toLowerCase() === 'medium' ? 'why-chance-med'
                      : 'why-chance-low';

        html =
            '<div class="why-structured">' +
                '<div class="why-row">' +
                    '<span class="why-label">Chance Level</span>' +
                    '<span class="why-val ' + chanceCls + '">' + m.chanceLevel + '</span>' +
                '</div>' +
                (m.userPct && m.userPct !== '—' ?
                '<div class="why-row">' +
                    '<span class="why-label">Your Percentile</span>' +
                    '<span class="why-val">' + m.userPct + '</span>' +
                '</div>' : '') +
                (m.cutoffVal ?
                '<div class="why-row">' +
                    '<span class="why-label">Last Year Cutoff</span>' +
                    '<span class="why-val">' + m.cutoffVal + '</span>' +
                '</div>' : '') +
                (m.diffText ?
                '<div class="why-row">' +
                    '<span class="why-label">Difference</span>' +
                    '<span class="why-val">' + m.diffText + '</span>' +
                '</div>' : '') +
                (m.seatType ?
                '<div class="why-row">' +
                    '<span class="why-label">Seat Category</span>' +
                    '<span class="why-val">' + m.seatType + '</span>' +
                '</div>' : '') +
                '<div class="why-explain-block">' +
                    '<div class="why-explain-heading">Explanation</div>' +
                    '<div class="why-explain-text">' + (m.explanation || '') + '</div>' +
                '</div>' +
                (m.websiteUrl ?
                '<div class="why-row why-website-row">' +
                    '<span class="why-label">Website</span>' +
                    '<a class="why-website-link" href="' + m.websiteUrl + '" target="_blank" rel="noopener noreferrer">Visit College Website ↗</a>' +
                '</div>' : '') +
            '</div>';
    } else {
        // Fallback for static scholarship modals 
        html = (m.reasons || []).map(function(r) {
            return '<div class="why-reason"><div class="why-text">' + r.text + '</div></div>';
        }).join('');
    }

    document.getElementById('modal-reasons').innerHTML = html;
    document.getElementById('modal-overlay').classList.add('open');
}

function closeAllModals() {
    document.getElementById('modal-overlay').classList.remove('open');
}

function closeModal(e) {
    if (e.target === document.getElementById('modal-overlay')) closeAllModals();
}

// ---------- KEYBOARD HANDLING FOR CHIPS ----------
function handleChipKey(e, el) {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleChip(el);
    }
}

function handleFilterKey(e, el) {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        filterActive(el);
    }
}

// ---------- HELPER: Get selected chips values ----------
function getSelectedChips(selector) {
    const values = [];
    document.querySelectorAll(selector).forEach(function(c) {
        if (c.dataset.branches) {
            c.dataset.branches.split(',').forEach(function(b) { values.push(b.trim()); });
        } else if (c.dataset.type) {
            values.push(c.dataset.type.trim());
        } else {
            values.push(c.textContent.trim());
        }
    });
    return values;
}

function selectAllChips(groupId) {
    document.querySelectorAll('#' + groupId + ' .chip').forEach(function(c) {
        c.classList.add('selected');
    });
}

function clearAllChips(groupId) {
    document.querySelectorAll('#' + groupId + ' .chip').forEach(function(c) {
        c.classList.remove('selected');
    });
}

// ---------- FORM VALIDATION (Counseling) ----------
function validateCounselingForm() {
    const percentile = document.getElementById('percentile');
    const percentileError = document.getElementById('percentileError');
    if (percentileError) percentileError.textContent = '';

    const val = parseFloat(percentile.value);
    if (!percentile.value || isNaN(val) || val < 0 || val > 100) {
        if (percentileError) percentileError.textContent = 'Please enter a valid percentile between 0 and 100';
        percentile.focus();
        return false;
    }
    return true;
}

// ---------- HANDLE COUNSELING SUBMIT ----------
async function handleCounselingSubmit(e) {
    e.preventDefault();
    if (!validateCounselingForm()) return;

    const btn = document.getElementById('counselingSubmit');
    btn.disabled = true;
    btn.innerHTML = '<span class="cc-spinner"></span> Searching colleges…';

    var aiPan = document.getElementById('aiInsightPanel');
    var cPan = document.getElementById('counselorChatPanel');
    var exBar = document.getElementById('resToolbarExtras');
    if (aiPan) { aiPan.style.display = 'none'; }
    if (cPan) { cPan.style.display = 'none'; }
    if (exBar) { exBar.style.display = 'none'; }
    var csi = document.getElementById('collegeSearchInput');
    if (csi) { csi.value = ''; }
    try { sessionStorage.removeItem('explainai_counselor_history'); } catch (eClr) { }

    const finalPercentile = parseFloat(document.getElementById('percentile').value);
    sessionStorage.setItem('inputPercentile', finalPercentile);

    const formData = {
        percentile: finalPercentile,
        category: document.getElementById('category').value,
        gender: document.getElementById('counselingGender').value,
        city: document.getElementById('city').value,
        branches: getSelectedChips('#branch-chips .chip.selected'),
        collegeTypes: (function() {
            var total  = document.querySelectorAll('#college-type-chips .chip').length;
            var sel    = document.querySelectorAll('#college-type-chips .chip.selected').length;
            // If all chips selected → no filter (show every college type including Other)
            if (sel === 0 || sel >= total) return [];
            return getSelectedChips('#college-type-chips .chip.selected');
        })()
    };

    // Save category and city AFTER formData is built so results header shows correct values
    sessionStorage.setItem('inputCategory', formData.category);
    sessionStorage.setItem('inputCity', formData.city);

    try {
        const response = await fetch(API_BASE + '/api/recommend/colleges', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (result.status === 'success') {
            renderCollegeResults(result.data, result.filter_note || null, null);
            showPage('results-counseling');
        } else if (result.status === 'no_results') {
            renderCollegeResults([], null, result.hint || null);
            showPage('results-counseling');
        } else {
            alert('Error: ' + (result.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Submission error:', error);
        alert('Failed to connect to the API. If you use Live Server, start the Flask backend (default port 5000) or open the app from the same host as the API.');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg> Get College Recommendations';
    }
}

// ---------- RENDER COLLEGE RESULTS — shows ALL colleges by default ----------
function renderCollegeResults(colleges, filterNote, noResultsHint) {
    var grid     = document.getElementById('resultsGrid');
    var countEl  = document.getElementById('resultsCount');
    var emptyEl  = document.getElementById('resEmpty');
    var bannerEl = document.getElementById('resScholarBanner');
    var showEl   = document.getElementById('resShowing');
    var exBar    = document.getElementById('resToolbarExtras');
    var aiPan    = document.getElementById('aiInsightPanel');
    if (!grid) return;

    grid.innerHTML = '';
    if (emptyEl)  emptyEl.style.display  = 'none';
    if (bannerEl) bannerEl.style.display = 'none';

    // Show/hide the filter info notice
    var noteEl = document.getElementById('resFilterNote');
    if (noteEl) {
        if (filterNote) {
            noteEl.textContent = filterNote;
            noteEl.style.display = '';
        } else {
            noteEl.style.display = 'none';
        }
    }

    if (!colleges || colleges.length === 0) {
        if (countEl) countEl.textContent = 'No Colleges Found';
        if (exBar) exBar.style.display = 'none';
        if (aiPan) aiPan.style.display = 'none';
        var ccP0 = document.getElementById('counselorChatPanel');
        if (ccP0) ccP0.style.display = 'none';
        if (emptyEl) {
            var msg = noResultsHint ||
                'No colleges found for your filters. Try changing your branch, city, or college type.';
            emptyEl.innerHTML =
                //'<div class="res-empty-icon">🔍</div>' +
                '<p class="res-empty-title">No Results Found</p>' +
                '<p class="res-empty-msg">' + msg + '</p>';
            emptyEl.style.display = '';
        }
        _setFilterCounts(0, 0, 0, 0);
        if (showEl) showEl.textContent = '';
        return;
    }

    // Split into chance groups
    var allHigh = [], allMed = [], allLow = [];
    colleges.forEach(function(c) {
        var ch = (c.chance || '').toLowerCase();
        if (ch === 'high')        allHigh.push(c);
        else if (ch === 'medium') allMed.push(c);
        else                      allLow.push(c);
    });

    // Store on grid for filter buttons to use
    grid._allHigh = allHigh;
    grid._allMed  = allMed;
    grid._allLow  = allLow;
    grid._all     = colleges;
    grid._activeFilter = 'all';

    if (exBar) exBar.style.display = 'flex';
    var cPan = document.getElementById('counselorChatPanel');
    if (cPan) cPan.style.display = APP_SERVER_CONFIG.ai_enabled ? 'block' : 'none';
    var saveBtn = document.getElementById('btnSavePredictionRun');
    var aiCards = document.getElementById('btnAiCardInsights');
    var ai2 = document.getElementById('btnAiGuidance');
    if (saveBtn) saveBtn.style.display = getCurrentUser() && getCurrentUser().id ? '' : 'none';
    if (aiCards) aiCards.style.display = APP_SERVER_CONFIG.ai_enabled ? '' : 'none';
    if (ai2) ai2.style.display = APP_SERVER_CONFIG.ai_enabled ? '' : 'none';
    if (APP_SERVER_CONFIG.ai_enabled) {
        _renderCounselorMessages();
    }

    // Update all counts
    _setFilterCounts(colleges.length, allHigh.length, allMed.length, allLow.length);

    // Heading
    if (countEl) countEl.textContent = colleges.length + ' College Recommendation' + (colleges.length !== 1 ? 's' : '') + ' Found';

    // Showing text
    if (showEl) showEl.textContent = 'All ' + colleges.length + ' colleges listed below';
    var dlBtn = document.getElementById('resDownloadBtn');
    if (dlBtn) dlBtn.style.display = colleges.length > 0 ? '' : 'none';

    if (bannerEl) bannerEl.style.display = '';

    // Reset filter chips to All
    document.querySelectorAll('#resultFilterChips .rfc').forEach(function(b) { b.classList.remove('rfc-active'); });
    var allBtn = document.querySelector('#resultFilterChips [data-filter="all"]');
    if (allBtn) allBtn.classList.add('rfc-active');

    // *** Show ALL colleges — no artificial 20 cap ***
    _renderCards(grid, colleges);

    // Update dashboard stats
    updateDashboardStats();
}

function _renderCards(grid, list) {
    grid.innerHTML = '';

    var liked    = _getLiked();
    var disliked = _getDisliked();

    // Filter out colleges the student marked Not Interested
    var filtered = list.filter(function(col) {
        var name   = col.college_name || 'Unknown College';
        var branch = col.branch       || '';
        var colKey = (name + '__' + branch).replace(/\s+/g, '_').toLowerCase().substring(0, 80);
        return !disliked.includes(colKey);
    });

    filtered.forEach(function(col, idx) {
        var card   = document.createElement('div');
        var chance = col.chance || 'Low';
        var chLow  = chance.toLowerCase();
        card.className = 'result-card rc-' + chLow;
        card.dataset.chance = chLow;

        var name   = col.college_name      || 'Unknown College';
        var branch = col.branch            || '';
        // City: take last part after comma if college name contains city
        var rawCity = col.city || '';
        var city   = rawCity.split(',').pop().trim();
        var ctype  = col.college_type      || '';
        var cutoff = col.cutoff_percentile != null ? col.cutoff_percentile : 0;
        var seat   = col.seat_type         || '';
        var reason = col.explanation       || '';

        // Unique key for like/dislike
        var colKey = (name + '__' + branch).replace(/\s+/g, '_').toLowerCase().substring(0, 80);

        var isLiked    = liked.includes(colKey);
        var isDisliked = disliked.includes(colKey);

        // Register modal data — structured plain-text, no emojis
        var mKey = 'rm_' + idx;
        var userPct   = parseFloat(sessionStorage.getItem('inputPercentile') || 0);
        var cutoffNum = parseFloat(cutoff) || 0;
        var diffNum   = userPct > 0 ? parseFloat((userPct - cutoffNum).toFixed(2)) : null;

        var diffText = '';
        if (diffNum !== null) {
            if (diffNum > 0) {
                diffText = 'You are ' + diffNum + ' percentile above the cutoff. Your score is higher than what was needed last year.';
            } else if (diffNum === 0) {
                diffText = 'Your percentile is exactly at the cutoff. Admission is possible but not guaranteed.';
            } else {
                diffText = 'You are ' + Math.abs(diffNum) + ' percentile below the cutoff. Admission is less likely, but cutoffs can change each year.';
            }
        }

        var plainExplanation = '';
        if (chLow === 'high') {
            plainExplanation = 'Your percentile is higher than the previous cutoff for this college and branch. Because of this, you have a good chance of getting admission in this course.';
        } else if (chLow === 'medium') {
            plainExplanation = 'Your percentile is close to the cutoff for this college and branch. You may get admission, but it is not fully certain. Keep this as a backup option.';
        } else {
            plainExplanation = 'Your percentile is below the cutoff for this college and branch. Getting admission here will be difficult, but cutoffs change every year so it is still worth applying.';
        }

        modals[mKey] = {
            title:       name + ' — ' + branch,
            subtitle:    (city ? city + '   ' : '') + (ctype || ''),
            chanceLevel: chance,
            userPct:     userPct > 0 ? userPct.toFixed(2) : '—',
            cutoffVal: cutoffNum > 0 ? parseFloat(cutoffNum.toFixed(2)) : cutoff,
            diffText:    diffText,
            explanation: plainExplanation,
            seatType:    seat,
            websiteUrl:  getCollegeUrl(name)
        };

        // Chance badge — text only
        var chanceLabel = chLow === 'high' ? 'High Chance' : chLow === 'medium' ? 'Medium Chance' : 'Low Chance';

        // Cutoff bar variables kept for any remaining usage
        var barMax    = Math.max(cutoffNum, userPct, 60);
        var cutoffPct = Math.min(100, (cutoffNum / barMax) * 100).toFixed(1);
        var userPctBar = Math.min(100, (userPct / barMax) * 100).toFixed(1);

        card.innerHTML =
            '<div class="rc-card-top">' +
                '<div class="rc-num">' + (idx + 1) + '</div>' +
                '<div class="rc-badge rc-badge-' + chLow + '">' + chanceLabel + '</div>' +
            '</div>' +
            '<div class="rc-body">' +
                '<div class="rc-name">' + name + '</div>' +
                '<div class="rc-branch">' + branch + '</div>' +
                '<div class="rc-meta-row">' +
                    (city  ? '<span class="rc-meta-item">' + city + '</span>' : '') +
                    (ctype ? '<span class="rc-meta-item rc-meta-type">' + ctype + '</span>' : '') +
                '</div>' +
            '</div>' +
            '<div class="rc-footer">' +
                '<div class="rc-why-row"></div>' +
                '<div class="rc-actions"></div>' +
            '</div>';

        var whyRow = card.querySelector('.rc-why-row');
        var actionsDiv = card.querySelector('.rc-actions');

        // Primary CTA: transparent "why this college" breakdown
        var whyBtn = document.createElement('button');
        whyBtn.type = 'button';
        whyBtn.className = 'rc-why';
        whyBtn.setAttribute('data-mkey', mKey);
        whyBtn.setAttribute('aria-label', 'See why this college was recommended — cutoff, your percentile, and plain explanation');
        whyBtn.title = 'Shows cutoff vs your percentile and a short, clear reason (no black box)';
        whyBtn.innerHTML =
            '<span class="rc-why-inner">' +
            '<svg class="rc-why-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
            '<circle cx="12" cy="12" r="10"/>' +
            '<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>' +
            '</svg>' +
            '<span class="rc-why-text"><span class="rc-why-line1">Why this college?</span><span class="rc-why-line2">Cutoff, your score &amp; plain English</span></span>' +
            '</span>';
        whyBtn.addEventListener('click', function() { openModal(this.getAttribute('data-mkey')); });
        whyRow.appendChild(whyBtn);

        // Visit Website button
        var websiteBtn = document.createElement('a');
        websiteBtn.href = getCollegeUrl(name);
        websiteBtn.target = '_blank';
        websiteBtn.rel = 'noopener noreferrer';
        websiteBtn.className = 'rc-website-btn';
        websiteBtn.textContent = 'Visit Website';
        actionsDiv.appendChild(websiteBtn);

        // Save button — text only, no emoji
        var likeBtn = document.createElement('button');
        likeBtn.className = 'rc-like' + (isLiked ? ' active-like' : '');
        likeBtn.textContent = isLiked ? 'Saved' : 'Save';
        likeBtn.title = isLiked ? 'Remove from saved' : 'Save this college';
        likeBtn.setAttribute('aria-label', 'Save');
        likeBtn.dataset.colKey    = colKey;
        likeBtn.dataset.colName   = name;
        likeBtn.dataset.colBranch = branch;
        likeBtn.addEventListener('click', function() {
            toggleLike(this, this.dataset.colKey, this.dataset.colName, this.dataset.colBranch);
            this.textContent = this.classList.contains('active-like') ? 'Saved' : 'Save';
        });
        actionsDiv.appendChild(likeBtn);

        // Not Interested button — text only, no emoji
        var dislikeBtn = document.createElement('button');
        dislikeBtn.className = 'rc-dislike' + (isDisliked ? ' active-dislike' : '');
        dislikeBtn.textContent = isDisliked ? 'Removed' : 'Not Interested';
        dislikeBtn.title = isDisliked ? 'Undo' : 'Mark as not interested';
        dislikeBtn.setAttribute('aria-label', 'Not Interested');
        dislikeBtn.dataset.colKey    = colKey;
        dislikeBtn.dataset.colName   = name;
        dislikeBtn.dataset.colBranch = branch;
        dislikeBtn.addEventListener('click', function() {
            var c = this.closest('.result-card');
            toggleDislike(this, this.dataset.colKey, this.dataset.colName, this.dataset.colBranch);
            // Hide the card immediately so student no longer sees it
            if (c) {
                c.style.transition = 'opacity 0.25s';
                c.style.opacity = '0';
                setTimeout(function() {
                    c.style.display = 'none';
                    _updateFilterCountsAfterHide();
                }, 260);
            }
        });
        actionsDiv.appendChild(dislikeBtn);

        grid.appendChild(card);
    });
}

// ---------- SMART MIX: balanced distribution across High/Med/Low ----------
function _smartMix(high, med, low, total) {
    var groups = [
        { arr: high, label: 'high' },
        { arr: med,  label: 'med'  },
        { arr: low,  label: 'low'  }
    ].filter(function(g) { return g.arr.length > 0; });

    if (groups.length === 0) return [];

    // Base allocation: divide total equally, guarantee at least 1 per non-empty group
    var slots = {};
    var base = Math.floor(total / groups.length);
    groups.forEach(function(g) { slots[g.label] = base; });

    // Distribute remainder
    var remainder = total - base * groups.length;
    for (var i = 0; i < remainder; i++) {
        slots[groups[i % groups.length].label]++;
    }

    // Cap at actual array length, redistribute leftovers
    var leftover = 0;
    groups.forEach(function(g) {
        var cap = g.arr.length;
        if (slots[g.label] > cap) {
            leftover += slots[g.label] - cap;
            slots[g.label] = cap;
        }
    });

    // Give leftover to groups that still have capacity
    if (leftover > 0) {
        groups.forEach(function(g) {
            if (leftover <= 0) return;
            var cap = g.arr.length - slots[g.label];
            var add = Math.min(cap, leftover);
            slots[g.label] += add;
            leftover -= add;
        });
    }

    // Build result: High first, then Med, then Low (interleaved for visual balance)
    var result = [];
    var hi = (high || []).slice(0, slots['high'] || 0);
    var me = (med  || []).slice(0, slots['med']  || 0);
    var lo = (low  || []).slice(0, slots['low']  || 0);

    // Interleave so user sees all levels immediately
    var maxLen = Math.max(hi.length, me.length, lo.length);
    for (var j = 0; j < maxLen; j++) {
        if (j < hi.length) result.push(hi[j]);
        if (j < me.length) result.push(me[j]);
        if (j < lo.length) result.push(lo[j]);
    }
    return result;
}

function filterResults(btn, level) {
    var grid   = document.getElementById('resultsGrid');
    var showEl = document.getElementById('resShowing');
    if (!grid) return;

    document.querySelectorAll('#resultFilterChips .rfc').forEach(function(b) { b.classList.remove('rfc-active'); });
    btn.classList.add('rfc-active');

    var list;
    if (level === 'all') {
        list = grid._all || [];
        if (showEl) showEl.textContent = 'All ' + list.length + ' colleges listed below';
    } else if (level === 'high') {
        list = grid._allHigh || [];
        if (showEl) showEl.textContent = list.length + ' High Chance college' + (list.length !== 1 ? 's' : '');
    } else if (level === 'medium') {
        list = grid._allMed || [];
        if (showEl) showEl.textContent = list.length + ' Medium Chance college' + (list.length !== 1 ? 's' : '');
    } else {
        list = grid._allLow || [];
        if (showEl) showEl.textContent = list.length + ' Low Chance college' + (list.length !== 1 ? 's' : '');
    }

    grid._activeFilter = level;

    var q = (document.getElementById('collegeSearchInput') && document.getElementById('collegeSearchInput').value || '').trim().toLowerCase();
    if (q) {
        var before = list.length;
        list = list.filter(function (c) {
            var n = (c.college_name || '').toLowerCase();
            var b = (c.branch || '').toLowerCase();
            return n.indexOf(q) !== -1 || b.indexOf(q) !== -1;
        });
        if (showEl) {
            showEl.textContent = list.length + ' match' + (list.length !== 1 ? 'es' : '') +
                ' for “' + q + '”' + (before !== list.length ? ' (of ' + before + ' in this tier)' : '');
        }
    }

    _renderCards(grid, list);
}

function _setFilterCounts(total, high, med, low) {
    var fa = document.getElementById('fc-all');
    var fh = document.getElementById('fc-high');
    var fm = document.getElementById('fc-med');
    var fl = document.getElementById('fc-low');
    if (fa) fa.textContent = total;
    if (fh) fh.textContent = high;
    if (fm) fm.textContent = med;
    if (fl) fl.textContent = low;

    // Update header summary pills
    var summary = document.getElementById('resChanceSummary');
    var rcsH = document.getElementById('rcs-high-n');
    var rcsM = document.getElementById('rcs-med-n');
    var rcsL = document.getElementById('rcs-low-n');
    if (rcsH) rcsH.textContent = high;
    if (rcsM) rcsM.textContent = med;
    if (rcsL) rcsL.textContent = low;
    if (summary && total > 0) summary.style.display = 'flex';
}

// ---------- RECALCULATE FILTER COUNTS AFTER A CARD IS HIDDEN ----------
function _updateFilterCountsAfterHide() {
    var grid = document.getElementById('resultsGrid');
    if (!grid || !grid._all) return;

    var disliked = _getDisliked();

    // Filter the original full data arrays, removing disliked entries
    function notDisliked(col) {
        var key = ((col.college_name || '') + '__' + (col.branch || ''))
            .replace(/\s+/g, '_').toLowerCase().substring(0, 80);
        return !disliked.includes(key);
    }

    var newAll  = (grid._all     || []).filter(notDisliked);
    var newHigh = (grid._allHigh || []).filter(notDisliked);
    var newMed  = (grid._allMed  || []).filter(notDisliked);
    var newLow  = (grid._allLow  || []).filter(notDisliked);

    // Update the stored arrays so filter buttons use correct data
    grid._all     = newAll;
    grid._allHigh = newHigh;
    grid._allMed  = newMed;
    grid._allLow  = newLow;

    // Update filter bar counts AND header pills
    _setFilterCounts(newAll.length, newHigh.length, newMed.length, newLow.length);

    // Update "X colleges listed below" text based on active filter
    var showEl = document.getElementById('resShowing');
    if (showEl) {
        var activeBtn = document.querySelector('#resultFilterChips .rfc.rfc-active');
        var level = activeBtn ? (activeBtn.dataset.filter || 'all') : 'all';
        if (level === 'all')         showEl.textContent = 'All ' + newAll.length + ' colleges listed below';
        else if (level === 'high')   showEl.textContent = newHigh.length + ' High Chance college'   + (newHigh.length !== 1 ? 's' : '');
        else if (level === 'medium') showEl.textContent = newMed.length  + ' Medium Chance college' + (newMed.length  !== 1 ? 's' : '');
        else                         showEl.textContent = newLow.length  + ' Low Chance college'    + (newLow.length  !== 1 ? 's' : '');
    }

    // Update heading count
    var countEl = document.getElementById('resultsCount');
    if (countEl) countEl.textContent = newAll.length + ' College Recommendation' + (newAll.length !== 1 ? 's' : '') + ' Found';

    updateDashboardStats();
}
function displayResultsMetadata() {
    // Read ONLY from sessionStorage — saved at submit time, never from live form element
    var percentile = sessionStorage.getItem('inputPercentile');
    var category   = sessionStorage.getItem('inputCategory') || 'OPEN';
    var city       = sessionStorage.getItem('inputCity')     || '';

    // Empty string means user selected All Maharashtra
    var cityLabel = (!city || city.trim() === '') ? 'All Maharashtra' : city;

    var pctEl  = document.getElementById('rpcPctVal');
    var catEl  = document.getElementById('rpcCatVal');
    var cityEl = document.getElementById('rpcCityVal');

    if (pctEl)  pctEl.textContent  = percentile ? parseFloat(percentile).toFixed(2) : '—';
    if (catEl)  catEl.textContent  = category || '—';
    if (cityEl) cityEl.textContent = cityLabel;
}

// ---------- SCHOLARSHIP FORM VALIDATION ----------
function validateScholarshipForm() {
    let valid = true;
    const income = document.getElementById('scholarIncome');
    const incomeError = document.getElementById('incomeError');
    const percentage = document.getElementById('scholarPercentage');
    const percentageError = document.getElementById('percentageError');

    if (incomeError) incomeError.textContent = '';
    if (percentageError) percentageError.textContent = '';

    if (!income.value || income.value < 0) {
        if (incomeError) incomeError.textContent = 'Please enter a valid income';
        valid = false;
    }
    if (!percentage.value || percentage.value < 0 || percentage.value > 100) {
        if (percentageError) percentageError.textContent = 'Percentage must be between 0 and 100';
        valid = false;
    }
    return valid;
}

// ---------- AUTO-FILL SCHOLARSHIP FORM FROM COUNSELING DATA ----------
function prefillScholarshipForm() {
    const savedCategory = sessionStorage.getItem('inputCategory');
    const counselGender = document.getElementById('counselingGender')
                          ? document.getElementById('counselingGender').value : null;

    let prefilled = false;

    if (savedCategory) {
        const catSelect = document.getElementById('scholarCategory');
        if (catSelect) {
            for (let i = 0; i < catSelect.options.length; i++) {
                if (catSelect.options[i].value === savedCategory) {
                    catSelect.selectedIndex = i;
                    prefilled = true;
                    break;
                }
            }
        }
    }

    if (counselGender) {
        const genSelect = document.getElementById('scholarGender');
        if (genSelect) {
            for (let i = 0; i < genSelect.options.length; i++) {
                if (genSelect.options[i].value === counselGender) {
                    genSelect.selectedIndex = i;
                    prefilled = true;
                    break;
                }
            }
        }
    }

    // No notice shown — silently prefill
}

// ---------- HANDLE SCHOLARSHIP SUBMIT ----------
async function handleScholarshipSubmit(e) {
    e.preventDefault();
    if (!validateScholarshipForm()) return;

    const btn = document.getElementById('scholarshipSubmit');
    btn.disabled = true;
    btn.innerHTML = '<span class="cc-spinner"></span> Finding scholarships...';

    const formData = {
        category:    document.getElementById('scholarCategory').value,
        income:      document.getElementById('scholarIncome').value,
        gender:      document.getElementById('scholarGender').value,
        domicile:    document.getElementById('scholarDomicile').value,
        disability:  document.getElementById('scholarDisability').value,
        percentage:  document.getElementById('scholarPercentage').value,
        minority:    document.getElementById('scholarMinority').value,
        yearOfStudy: parseInt(document.getElementById('scholarYear').value) || 1
    };

    try {
        const res = await fetch(API_BASE + '/api/recommend/scholarships', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-User-Id': localStorage.getItem('user_id') || ''
            },
            body: JSON.stringify(formData)
        });
        const json = await res.json();
        if (json.status === 'success') {
            renderScholarshipResults(json.data, json.total_eligible, formData);
            showPage('results-scholarship');
        } else {
            alert('Error: ' + (json.error || 'Something went wrong.'));
        }
    } catch (error) {
        console.error('Scholarship error:', error);
        alert('Failed to connect. Make sure the Flask server is running.');
    } finally {
        btn.disabled = false;
        btn.innerHTML = 'Find My Scholarships';
    }
}

// ---------- RENDER SCHOLARSHIP RESULTS ----------
function renderScholarshipResults(data, totalEligible, formData) {
    const eligible = data.filter(function(s) { return s.eligible; });

    // Filter out any scholarships the student marked Not Interested FIRST,
    // so that counts, title, and banner all reflect what is actually visible.
    var scholarDisliked = _getScholarDisliked();
    var visibleEligible = eligible.filter(function(s) {
        var key = 'scholar__' + String(s.id || s.name || '').replace(/\s+/g, '_').toLowerCase().substring(0, 60);
        return !scholarDisliked.includes(key);
    });

    var visibleCount = visibleEligible.length;

    // Title reflects how many scholarships are actually shown
    document.getElementById('scholarshipResultsTitle').textContent =
        visibleCount > 0
            ? visibleCount + ' Scholarship' + (visibleCount > 1 ? 's' : '') + ' Found For You'
            : 'No Eligible Scholarships Found';

    document.getElementById('scholarshipMeta').textContent =
        formData.category + ' | Income Rs.' + Number(formData.income).toLocaleString('en-IN') +
        ' | ' + formData.gender + ' | ' + formData.percentage + '% in 12th' +
        ' | Year ' + formData.yearOfStudy;

    window._lastScholarFormData = formData;
    window._scholarApplyPayload = {};

    // Save visible count for dashboard stat
    localStorage.setItem(_userStorageKey('explainai_scholar_total'), visibleCount);
    updateDashboardStats();

    // Banner also reflects visible count
    const banner     = document.getElementById('scholarshipSummaryBanner');
    const bannerText = document.getElementById('scholarshipSummaryText');
    if (visibleCount > 0) {
        bannerText.innerHTML = 'You qualify for <strong>' + visibleCount +
            ' scholarship' + (visibleCount > 1 ? 's' : '') +
            '</strong>. Apply on the respective portals before the deadline closes.';
        banner.style.display = 'flex';
    } else {
        banner.style.display = 'none';
    }

    // Render cards (or appropriate empty state)
    document.getElementById('scholarshipCardsContainer').innerHTML =
        visibleCount > 0
            ? visibleEligible.map(function(s) { return buildScholarshipCard(s, true, formData); }).join('')
            : eligible.length > 0
                ? '<p style="text-align:center; padding:40px 0; color:#555">You\'ve hidden all matching scholarships. Refresh to see them again.</p>'
                : '<p style="text-align:center; padding:40px 0; color:#555">No scholarships match your profile.</p>';

    // Always hide not-eligible section — ineligible scholarships are not shown to students
    const notEligSection = document.getElementById('scholarshipNotEligibleSection');
    if (notEligSection) notEligSection.style.display = 'none';
}

function buildScholarshipCard(s, eligible, formData) {
    formData = formData || {};
    window._scholarApplyPayload = window._scholarApplyPayload || {};
    window._scholarApplyPayload[s.id] = {
        name: s.name || '',
        portal_url: s.portal_url || '',
        documents: s.documents || [],
        category: formData.category || ''
    };
    var deadlineTagClass = s.deadline_status === 'estimated' ? 'scholar-tag tag-estimated'
                         : s.deadline_status === 'urgent'    ? 'scholar-tag tag-red'
                         : s.deadline_status === 'open'      ? 'scholar-tag tag-green'
                         : 'scholar-tag tag-blue';
    var deadlineIcon = s.deadline_status === 'estimated' ? '⚠️ ' : '';
    var deadlineText = deadlineIcon + (s.deadline_text || '');

    // Documents — hidden list, shown on button click
    var docsHtml = '';
    if (s.documents && s.documents.length > 0) {
        var docItems = s.documents.map(function(d) {
            return '<li style="margin-bottom:5px;color:#444;font-size:12px">' + d + '</li>';
        }).join('');
        docsHtml =
            '<div class="scholar-docs" style="margin-top:10px">' +
                '<button type="button" onclick="toggleDocs(this)" ' +
                    'style="background:transparent; border:1px solid #c7c2f8; ' +
                    'color:#4f46e5; border-radius:6px; padding:4px 12px; font-size:12px; cursor:pointer;">' +
                    'Documents needed (' + s.documents.length + ')' +
                '</button>' +
                '<ul class="docs-list" style="display:none; margin:8px 0 0 0; padding-left:18px;">' +
                    docItems +
                '</ul>' +
            '</div>';
    }

    // Why button — always shown, clear label
    var mKey = 'scholar_' + s.id;
    if (!window._scholarModals) window._scholarModals = {};
    window._scholarModals[mKey] = {
        title:    s.name,
        subtitle: s.source + ' Portal  |  ' + (s.amount || ''),
        eligible: eligible,
        reasons:  s.reasons || []
    };
    var whyBtnHtml = eligible
        ? '<button type="button" class="why-btn why-btn--featured" onclick="openScholarModal(\'' + mKey + '\')" aria-label="See why this scholarship was matched">' +
            '<span class="rc-why-inner">' +
            '<svg class="rc-why-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
            '<circle cx="12" cy="12" r="10"/>' +
            '<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>' +
            '</svg>' +
            '<span class="rc-why-text"><span class="rc-why-line1">Why this scholarship?</span><span class="rc-why-line2">Open eligibility breakdown</span></span>' +
            '</span></button>'
        : '';

    var aiScholarBtn = (eligible && APP_SERVER_CONFIG.ai_enabled)
        ? '<button type="button" class="res-download-btn" style="margin-top:8px;font-size:12px;padding:6px 12px" onclick="requestScholarshipApplyGuide(' + Number(s.id) + ')">AI: how to apply</button>'
        : '';

    // First reason shown inline under tags — dark color so it's visible
    var reasonText = s.reasons && s.reasons.length > 0 ? s.reasons[0] : '';
    var sourceLabel = s.source === 'NSP' ? 'NSP' : s.source === 'MahaDBT' ? 'MH' : s.source;

    return '<div class="scholar-card" style="' + (eligible ? '' : 'opacity:0.55') + '" id="scholar-card-' + s.id + '">' +
        '<div class="scholar-icon" style="font-size:11px;font-weight:700;letter-spacing:0.5px;color:#444">' + sourceLabel + '</div>' +
        '<div class="scholar-body">' +
            '<div class="scholar-name">' + s.name + '</div>' +
            '<div class="scholar-source">' + s.source + ' Portal</div>' +
            '<div class="scholar-tags">' +
                '<span class="scholar-tag ' + (eligible ? 'tag-green' : '') + '" ' +
                    'style="' + (eligible ? '' : 'background:rgba(220,38,38,0.1);color:#dc2626') + '">' +
                    (eligible ? 'Eligible' : 'Not Eligible') +
                '</span>' +
                (deadlineText
                    ? '<span class="' + deadlineTagClass + '">' + deadlineText + '</span>'
                    : '') +
            '</div>' +
            (reasonText ? '<div style="font-size:12px;color:#555;margin-top:6px">' + reasonText + '</div>' : '') +
            docsHtml +
            whyBtnHtml +
            aiScholarBtn +
            buildScholarshipActionBtns(s) +
        '</div>' +
        '<div class="scholar-amount">' +
            '<span class="amount-num">' + (s.amount || '') + '</span>' +
            (eligible
                ? '<a href="' + s.portal_url + '" target="_blank" rel="noopener" ' +
                  'style="display:inline-block;margin-top:10px;font-size:13px;color:#4f46e5;text-decoration:underline;font-weight:600">Apply Now</a>'
                : '') +
        '</div>' +
    '</div>';
}

function toggleDocs(btn) {
    var list = btn.nextElementSibling;
    if (!list) return;
    if (list.style.display === 'none') {
        list.style.display = 'block';
        btn.textContent = btn.textContent.replace('Documents needed', 'Hide documents');
    } else {
        list.style.display = 'none';
        btn.textContent = btn.textContent.replace('Hide documents', 'Documents needed');
    }
}

function openScholarModal(mKey) {
    var m = window._scholarModals && window._scholarModals[mKey];
    if (!m) return;

    var kickerEl = document.getElementById('modal-kicker');
    if (kickerEl) {
        kickerEl.textContent = 'Scholarship match — why you see this';
    }
    document.getElementById('modal-title').textContent    = m.title;
    document.getElementById('modal-subtitle').textContent = m.subtitle;

    var statusHtml = '<div style="margin-bottom:12px;font-weight:600;color:' +
        (m.eligible ? '#059669' : '#dc2626') + '">' +
        (m.eligible ? 'You are eligible for this scholarship.' : 'You do not qualify for this scholarship.') +
        '</div>';

    var headingHtml = '<div style="font-size:11px;color:#888;margin-bottom:8px;' +
        'text-transform:uppercase;letter-spacing:0.5px">' +
        (m.eligible ? 'Reasons you qualify:' : 'Reasons you do not qualify:') + '</div>';

    var reasonsHtml = (m.reasons || []).map(function(r) {
        return '<div class="why-reason"><div class="why-text">' + r + '</div></div>';
    }).join('');

    document.getElementById('modal-reasons').innerHTML = statusHtml + headingHtml + reasonsHtml;
    document.getElementById('modal-overlay').classList.add('open');
}


// ---------- SCHOLARSHIP SAVE / NOT INTERESTED ----------
function _getScholarLiked()    { try { return JSON.parse(localStorage.getItem(_userStorageKey('explainai_scholar_liked'))    || '[]'); } catch(e) { return []; } }
function _getScholarDisliked() { try { return JSON.parse(localStorage.getItem(_userStorageKey('explainai_scholar_disliked')) || '[]'); } catch(e) { return []; } }
function _saveScholarLiked(arr)    { localStorage.setItem(_userStorageKey('explainai_scholar_liked'),    JSON.stringify(arr)); }
function _saveScholarDisliked(arr) { localStorage.setItem(_userStorageKey('explainai_scholar_disliked'), JSON.stringify(arr)); }

function buildScholarshipActionBtns(s) {
    var key = 'scholar__' + String(s.id || s.name || '').replace(/\s+/g, '_').toLowerCase().substring(0, 60);
    var isLiked    = _getScholarLiked().includes(key);
    var isDisliked = _getScholarDisliked().includes(key);
    return '<div class="scholar-actions" style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap">' +
        '<button type="button" ' +
            'id="scholar-save-' + key + '" ' +
            'class="rc-like' + (isLiked ? ' active-like' : '') + '" ' +
            'onclick="toggleScholarSave(this,\'' + key + '\',\'' + (s.name || '').replace(/'/g, '') + '\')">' +
            (isLiked ? 'Saved' : 'Save') +
        '</button>' +
        '<button type="button" ' +
            'id="scholar-nope-' + key + '" ' +
            'class="rc-dislike' + (isDisliked ? ' active-dislike' : '') + '" ' +
            'onclick="toggleScholarNope(this,\'' + key + '\',\'' + (s.name || '').replace(/'/g, '') + '\')">' +
            (isDisliked ? 'Removed' : 'Not Interested') +
        '</button>' +
    '</div>';
}

function toggleScholarSave(btn, key, name) {
    var liked    = _getScholarLiked();
    var disliked = _getScholarDisliked();
    var isLiked  = liked.includes(key);
    var card     = btn.closest('.scholar-card');
    var nopeBtn  = card ? card.querySelector('.rc-dislike') : null;

    if (isLiked) {
        _saveScholarLiked(liked.filter(function(k) { return k !== key; }));
        btn.classList.remove('active-like');
        btn.textContent = 'Save';
    } else {
        liked.push(key);
        _saveScholarLiked(liked);
        _saveScholarDisliked(disliked.filter(function(k) { return k !== key; }));
        btn.classList.add('active-like');
        btn.textContent = 'Saved';
        if (nopeBtn) { nopeBtn.classList.remove('active-dislike'); nopeBtn.textContent = 'Not Interested'; }
        _addActivity('Saved scholarship: ' + name);
    }
    updateDashboardStats();
}

function toggleScholarNope(btn, key, name) {
    var liked    = _getScholarLiked();
    var disliked = _getScholarDisliked();
    var isNoped  = disliked.includes(key);
    var card     = btn.closest('.scholar-card');

    if (isNoped) {
        _saveScholarDisliked(disliked.filter(function(k) { return k !== key; }));
    } else {
        disliked.push(key);
        _saveScholarDisliked(disliked);
        _saveScholarLiked(liked.filter(function(k) { return k !== key; }));
        _addActivity('Not Interested: ' + name);
        // Hide the card immediately, then update the banner count
        if (card) {
            card.style.transition = 'opacity 0.25s';
            card.style.opacity = '0';
            setTimeout(function() {
                card.style.display = 'none';
                _updateScholarshipBanner();
            }, 260);
        }
    }
    updateDashboardStats();
}

// Recount visible scholarship cards and update the summary banner
function _updateScholarshipBanner() {
    var container = document.getElementById('scholarshipCardsContainer');
    if (!container) return;
    var visible = 0;
    container.querySelectorAll('.scholar-card').forEach(function(c) {
        if (c.style.display !== 'none') visible++;
    });
    var bannerText = document.getElementById('scholarshipSummaryText');
    var banner     = document.getElementById('scholarshipSummaryBanner');
    var titleEl    = document.getElementById('scholarshipResultsTitle');
    if (visible > 0) {
        if (bannerText) bannerText.innerHTML = 'You qualify for <strong>' + visible +
            ' scholarship' + (visible > 1 ? 's' : '') +
            '</strong>. Apply on the respective portals before the deadline closes.';
        if (banner) banner.style.display = 'flex';
        if (titleEl) titleEl.textContent = visible + ' Scholarship' + (visible > 1 ? 's' : '') + ' Found For You';
    } else {
        if (banner) banner.style.display = 'none';
        if (titleEl) titleEl.textContent = 'No Eligible Scholarships Found';
    }
    // Update dashboard scholarship count
    localStorage.setItem(_userStorageKey('explainai_scholar_total'), visible);
    updateDashboardStats();
}

// ---------- HAMBURGER MENU & INITIAL SETUP ----------
document.addEventListener('DOMContentLoaded', function() {
    initEaTheme();
    initSeoFromLocation();
    var collegeSearchInput = document.getElementById('collegeSearchInput');
    if (collegeSearchInput) {
        collegeSearchInput.addEventListener('input', function () {
            var btn = document.querySelector('#resultFilterChips .rfc.rfc-active');
            if (!btn || !document.getElementById('resultsGrid') || !document.getElementById('resultsGrid')._all) return;
            filterResults(btn, btn.dataset.filter || 'all');
        });
    }
    var counselorInput = document.getElementById('counselorInput');
    if (counselorInput) {
        counselorInput.addEventListener('keydown', function (ev) {
            if (ev.key === 'Enter') {
                ev.preventDefault();
                sendCounselorChat();
            }
        });
    }
    const footerYear = document.getElementById('site-footer-year');
    if (footerYear) {
        footerYear.textContent = '\u00A9 ' + new Date().getFullYear() + ' ExplainAI';
    }

    const navLinks = document.getElementById('navLinks');
    if (navLinks) {
        navLinks.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                if (typeof bootstrap !== 'undefined' && window.innerWidth < 992) {
                    var inst = bootstrap.Collapse.getInstance(navLinks);
                    if (inst) inst.hide();
                }
            });
        });
    }

    // Add keyboard handlers to chips
    document.querySelectorAll('.chip').forEach(chip => {
        chip.setAttribute('tabindex', '0');
        chip.setAttribute('role', 'button');
        chip.addEventListener('keydown', (e) => handleChipKey(e, chip));
    });
    document.querySelectorAll('.filter-chip').forEach(chip => {
        chip.setAttribute('tabindex', '0');
        chip.setAttribute('role', 'button');
        chip.addEventListener('keydown', (e) => handleFilterKey(e, chip));
    });

    // If results page is active on load, show metadata
    if (document.getElementById('page-results-counseling').classList.contains('active')) {
        displayResultsMetadata();
    }

    // On load: ALWAYS open home page. Auth state is synced quietly in background.
    (async () => {
        await refreshAppServerConfig();
        try {
            const res = await fetch(`${API_BASE}/api/auth/me`, { credentials: 'include' });
            if (res.ok) {
                const result = await res.json();
                if (result.status === 'success' && result.user) {
                    const u = result.user;
                    setUserLoggedIn(true);
                    setCurrentUser({ id: u.id, name: u.full_name, email: u.email, phone: u.phone || '' });
                    updateSaveRunButtonVisibility();
                } else {
                    localStorage.removeItem('explainai_user_logged_in');
                    localStorage.removeItem('explainai_user');
                }
            } else {
                localStorage.removeItem('explainai_user_logged_in');
                localStorage.removeItem('explainai_user');
            }
        } catch (e) {
            // Backend unreachable — keep localStorage state as-is
        }
        updateNavBar();
        showPage('home', true);
    })();
});

async function downloadCollegeList() {
    var grid = document.getElementById('resultsGrid');
    if (!grid) return;
    var colleges = grid._all || [];
    if (colleges.length === 0) { alert('No colleges to download.'); return; }

    var btn = document.getElementById('resDownloadBtn');
    var prevText = btn ? btn.textContent : '';
    try {
        if (btn) {
            btn.disabled = true;
            btn.textContent = 'Loading PDF\u2026';
        }
        await ensureJsPdfLoaded();
    } catch (err) {
        alert('Could not load PDF library. Check your internet connection and try again.');
        if (btn) {
            btn.disabled = false;
            btn.textContent = prevText;
        }
        return;
    }

    if (typeof window.jspdf === 'undefined' || typeof window.jspdf.jsPDF === 'undefined') {
        alert('PDF library not available. Please try again.');
        if (btn) {
            btn.disabled = false;
            btn.textContent = prevText;
        }
        return;
    }

    try {
    var user       = getCurrentUser();
    var userName   = (user && user.name)  ? user.name  : 'Student';
    var userEmail  = (user && user.email) ? user.email : '';
    var userPhone  = (user && user.phone) ? user.phone : '';
    var percentile = sessionStorage.getItem('inputPercentile') || '-';
    var category   = sessionStorage.getItem('inputCategory')   || '-';
    var city       = sessionStorage.getItem('inputCity')       || 'All Maharashtra';
    var today      = new Date().toLocaleDateString('en-IN', { day:'2-digit', month:'long', year:'numeric' });

    var high = colleges.filter(function(c){ return (c.chance||'').toLowerCase() === 'high'; });
    var med  = colleges.filter(function(c){ return (c.chance||'').toLowerCase() === 'medium'; });
    var low  = colleges.filter(function(c){ return (c.chance||'').toLowerCase() === 'low'; });

    var doc   = new window.jspdf.jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
    var pageW = doc.internal.pageSize.getWidth();
    var margin = 12;
    var y = 14;

    // ── Title ──
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(16);
    doc.setTextColor(17, 17, 17);
    doc.text('College Recommendation List', margin, y);
    y += 5;
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(8);
    doc.setTextColor(140, 140, 140);
    doc.text('Prepared by ExplainAI   |   ' + today, margin, y);

    // ── Student info box ──
    y += 7;
    doc.setFillColor(245, 245, 245);
    doc.setDrawColor(200, 200, 200);
    doc.roundedRect(margin, y, pageW - margin * 2, 14, 1, 1, 'FD');
    var col1 = margin + 3;
    doc.setFontSize(7);
    doc.setTextColor(140, 140, 140);
    doc.text('STUDENT NAME', col1,       y + 4);
    doc.text('EMAIL',        col1 + 48,  y + 4);
    doc.text('PHONE',        col1 + 108, y + 4);
    doc.text('PERCENTILE',   col1 + 152, y + 4);
    doc.text('CATEGORY',     col1 + 180, y + 4);
    doc.text('CITY',         col1 + 210, y + 4);
    doc.setFontSize(9);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(17, 17, 17);
    doc.text(userName, col1, y + 10);
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(8);
    if (userEmail) doc.text(userEmail,     col1 + 48,  y + 10);
    if (userPhone) doc.text(userPhone,     col1 + 108, y + 10);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(192, 57, 11);
    doc.setFontSize(11);
    doc.text(String(percentile),           col1 + 152, y + 11);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(17, 17, 17);
    doc.setFontSize(8);
    doc.text(String(category),             col1 + 180, y + 10);
    doc.text(String(city),                 col1 + 210, y + 10);

    // ── Important note ──
    y += 19;
    doc.setFillColor(255, 251, 235);
    doc.setDrawColor(245, 158, 11);
    doc.rect(margin, y, pageW - margin * 2, 7, 'FD');
    doc.setFontSize(7.5);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(120, 53, 15);
    doc.text('Important Note:', margin + 2, y + 4.5);
    doc.setFont('helvetica', 'normal');
    doc.text('You may modify this cutoff list as per your preferences and choice of branch, college, or category.', margin + 24, y + 4.5);

    var aiSummaryPdf = '';
    try { aiSummaryPdf = sessionStorage.getItem('explainai_last_ai_summary') || ''; } catch (eAi) { }
    y += 10;
    if (aiSummaryPdf) {
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(9);
        doc.setTextColor(17, 17, 17);
        doc.text('Counselling summary (last AI / offline insight)', margin, y);
        y += 4;
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(7.1);
        doc.setTextColor(55, 65, 85);
        var aiLines = doc.splitTextToSize(_stripMdBold(aiSummaryPdf).substring(0, 4500), pageW - margin * 2);
        doc.text(aiLines, margin, y);
        y += aiLines.length * 3.35 + 3;
    }

    // ── Summary line ──
    doc.setFontSize(8);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(60, 60, 60);
    // Color-coded legend line
    var lx = margin;
    doc.setFontSize(8);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(17, 17, 17);
    doc.text('Total: ' + colleges.length + ' colleges', lx, y);
    lx += 44;
    doc.setFillColor(34, 197, 94);   doc.circle(lx, y - 1.2, 1.8, 'F');
    doc.setTextColor(6, 95, 70);     doc.text('High Chance: ' + high.length, lx + 3.5, y);
    lx += 46;
    doc.setFillColor(234, 179, 8);   doc.circle(lx, y - 1.2, 1.8, 'F');
    doc.setTextColor(120, 53, 15);   doc.text('Medium Chance: ' + med.length, lx + 3.5, y);
    lx += 54;
    doc.setFillColor(239, 68, 68);   doc.circle(lx, y - 1.2, 1.8, 'F');
    doc.setTextColor(127, 29, 29);   doc.text('Low Chance: ' + low.length, lx + 3.5, y);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(60, 60, 60);

    // ── Build table rows ──
    // Columns: College Code | Name of College | Status | Location | Branch | Category | Cutoff
    // NO Chance column — 3 colored sections distinguish groups
    // Section header row = bold label on light section color
    // Data rows = alternating shades within section color

    // Section colors — light only, no dark colors on rows
    var SEC_HIGH_BG  = [209, 250, 229];  // green-100
    var SEC_HIGH_TX  = [6,   95,  70];   // green-900 (for section header text)
    var ROW_HIGH_E   = [240, 253, 244];  // green-50  (even rows)
    var ROW_HIGH_O   = [220, 252, 231];  // green-100 (odd rows)

    var SEC_MED_BG   = [254, 243, 199];  // yellow-100
    var SEC_MED_TX   = [120, 53,  15];   // yellow-900
    var ROW_MED_E    = [255, 253, 235];  // yellow-50
    var ROW_MED_O    = [254, 249, 195];  // yellow-100

    var SEC_LOW_BG   = [254, 226, 226];  // red-100
    var SEC_LOW_TX   = [127, 29,  29];   // red-900
    var ROW_LOW_E    = [255, 241, 242];  // red-50
    var ROW_LOW_O    = [254, 232, 232];  // red-100

    var allRows = [];
    var serial  = 0;

    function addSection(label, list, secBg, secTx, evenBg, oddBg) {
        if (!list.length) return;
        // No section header rows — row background color alone distinguishes chance level
        list.forEach(function(c, i) {
            serial++;
            var bg = i % 2 === 0 ? evenBg : oddBg;
            var cityDisp = (c.city || '').split(',').pop().trim();
            var cutoff   = c.cutoff_percentile != null ? parseFloat(c.cutoff_percentile).toFixed(2) : '-';
            var code     = (c.college_code && c.college_code !== '') ? c.college_code : String(serial);
            allRows.push({
                cells: [
                    code,
                    c.college_name || '',
                    c.college_type || '',
                    cityDisp,
                    c.branch       || '',
                    c.seat_type    || '',
                    cutoff
                ],
                bg:        bg,
                textColor: [17, 17, 17],
                isSection: false
            });
        });
    }

    addSection('HIGH CHANCE',   high, SEC_HIGH_BG, SEC_HIGH_TX, ROW_HIGH_E, ROW_HIGH_O);
    addSection('MEDIUM CHANCE', med,  SEC_MED_BG,  SEC_MED_TX,  ROW_MED_E,  ROW_MED_O);
    addSection('LOW CHANCE',    low,  SEC_LOW_BG,  SEC_LOW_TX,  ROW_LOW_E,  ROW_LOW_O);

    var tableBody = allRows.map(function(r) { return r.cells; });

    y += 4;
    doc.autoTable({
        startY: y,
        margin: { left: margin, right: margin },
        head: [['College Code', 'Name of College', 'Status', 'Location', 'Branch', 'Category', 'Cutoff']],
        body: tableBody,
        styles: {
            fontSize:    8,
            cellPadding: 2.5,
            overflow:    'linebreak',
            valign:      'middle',
            textColor:   [17, 17, 17]
        },
        headStyles: {
            fillColor: [51, 51, 51],
            textColor: [255, 255, 255],
            fontStyle: 'bold',
            fontSize:  8
        },
        columnStyles: {
            0: { cellWidth: 18, halign: 'center' },  // College Code
            1: { cellWidth: 90 },                    // Name of College
            2: { cellWidth: 30 },                    // Status
            3: { cellWidth: 28 },                    // Location
            4: { cellWidth: 50 },                    // Branch
            5: { cellWidth: 24 },                    // Category
            6: { cellWidth: 19, halign: 'right' }    // Cutoff
        },
        didParseCell: function(data) {
            if (data.section !== 'body') return;
            var row = allRows[data.row.index];
            if (!row) return;
            data.cell.styles.fillColor = row.bg;
            data.cell.styles.textColor = row.textColor;
            if (row.isSection) {
                data.cell.styles.fontStyle = 'bold';
                data.cell.styles.fontSize  = 8;
            }
        },
        didDrawPage: function(data) {
            var pg = data.pageNumber;
            doc.setFontSize(7);
            doc.setTextColor(160, 160, 160);
            doc.text(
                'ExplainAI  |  Cutoffs from DTE Maharashtra CAP 2025 data  |  Page ' + pg,
                margin, doc.internal.pageSize.getHeight() - 6
            );
        }
    });

    var safeName = (userName || 'Student').replace(/[^a-zA-Z0-9_\- ]/g, '').trim().replace(/\s+/g, '_');
    doc.save('CollegeList_' + safeName + '.pdf');
    } catch (genErr) {
        alert('Something went wrong while creating the PDF. Please try again.');
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.textContent = prevText;
        }
    }
}