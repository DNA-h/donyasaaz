import logging
import time
import math
from models.crawlers import *
from models.models import Price, Link, MusicItem
from constance import config
import random
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

crawlers = {"digiavl.com": digiavl_com.digiavl,
            "www.audiobashiryan.com": www_audiobashiryan_com.audiobashiryan, "www.charge-e.ir": www_charge_e_ir.charge,
            "www.namayeshgah.ir": www_namayeshgah_ir.namayeshgah, "www.avazeto.com": www_avazeto_com.avazeto,
            "www.cids.ir": www_cids_ir.cids, "simasot.com": simasot_com.simasot,
            "guitaro.ir": guitaro_ir.guitaro, "www.gamingtools.ir": www_gamingtools_ir.gamingtools,
            "amirdada.ir": amirdada_ir.amirdada, "naxhome.com": naxhome_com.naxhome,
            "solalestore.com": solalestore_com.solalestore, "melodux.com": melodux_com.melodux,
            "divar.ir": divar_ir.divar, "mlodica.ir": mlodica_ir.mlodica, "danakadeh.ir": danakadeh_ir.danakadeh,
            "navapercussion.ir": navapercussion_ir.navapercussion, "www.pianodorsa.com": www_pianodorsa_com.pianodorsa,
            "zoomlook.ir": zoomlook_ir.zoomlook, "www.saio.ir": www_saio_ir.saio,
            "zooya.ir": zooya_ir.zooya, "isfahanguitar.ir": isfahanguitar_ir.isfahanguitar,
            "yekharid.com": yekharid_com.yekharid, "rashnookala.com": rashnookala_com.rashnookala,
            "kalapage.ir": kalapage_ir.kalapage, "www.pianopars.com": www_pianopars_com.pianopars,
            "berozkala.com": berozkala_com.berozkala, "mashadkala.com": mashadkala_com.mashadkala,
            "msi-iran.com": msi_iran_com.msi_iran, "narestan.com": narestan_com.narestan,
            "harpmusical.com": harpmusical_com.harpmusical, "gooshidan.com": gooshidan_com.gooshidan,
            "www.iranaliexpress.ir": www_iranaliexpress_ir.iranaliexpress, "maralkish.ir": maralkish_ir.maralkish,
            "www.takinmall.com": www_takinmall_com.takinmall, "best-sound.ir": best_sound_ir.best_sound,
            "tehrankorg.com": tehrankorg_com.tehrankorg, "bazarchehsonati.com": bazarchehsonati_com.bazarchehsonati,
            "www.gatekala.ir": www_gatekala_ir.gatekala, "kadoyee.com": kadoyee_com.kadoyee,
            "irandrum.com": irandrum_com.irandrum, "tehrecorder.net": tehrecorder_net.tehrecorder,
            "cafekaala.ir": cafekaala_ir.cafekaala, "www.sazotar.com": www_sazotar_com.sazotar,
            "chechilas.com": chechilas_com.chechilas, "echochi.ir": echochi_ir.echochi,
            "www.itgheymat.com": www_itgheymat_com.itgheymat, "vgkala.com": vgkala_com.vgkala,
            "avazonline.ir": avazonline_ir.avazonline, "www.kalasabad.com": www_kalasabad_com.kalasabad,
            "faryadariyaei.com": faryadariyaei_com.faryadariyaei, "www.baya.ir": www_baya_ir.baya,
            "pianonava.com": pianonava_com.pianonava, "honaryab.com": honaryab_com.honaryab,
            "dpcomusic.com": dpcomusic_com.dpcomusic, "guitarstore.ir": guitarstore_ir.guitarstore,
            "www.kalavard.com": www_kalavard_com.kalavard, "www.iranvachar.ir": www_iranvachar_ir.iranvachar,
            "delnavazgallery.ir": delnavazgallery_ir.delnavazgallery, "thisone.ir": thisone_ir.thisone,
            "www.irofferr.cclip.ir": www_irofferr_cclip_ir.irofferr_cclip, "pickmusic.ir": pickmusic_ir.pickmusic,
            "saziha.ir": saziha_ir.saziha, "hoseinshop.ir": hoseinshop_ir.hoseinshop,
            "narix.ir": narix_ir.narix, "irtoshiba8.com": irtoshiba8_com.irtoshiba8,
            "ejanebi.com": ejanebi_com.ejanebi, "iran-canon.com": iran_canon_com.iran_canon,
            "www.noteahang.com": www_noteahang_com.noteahang, "www.tkadak.com": www_tkadak_com.tkadak,
            "sazmarket.com": sazmarket_com.sazmarket, "melodydj.ir": melodydj_ir.melodydj,
            "makeapurchase.ir": makeapurchase_ir.makeapurchase, "kemex.one": kemex_one.kemex,
            "harmonicatools.com": harmonicatools_com.harmonicatools, "harmonicand.ir": harmonicand_ir.harmonicand,
            "sazdahani.net": sazdahani_net.sazdahani, "pianotanin.com": pianotanin_com.pianotanin,
            "kookgallery.com": kookgallery_com.kookgallery, "sazgah.com": sazgah_com.sazgah,
            "www.yasertebat.com": www_yasertebat_com.yasertebat, "pexkala.com": pexkala_com.pexkala,
            "www.apple-nic.com": www_apple_nic_com.apple_nic, "payam-art.com": payam_art_com.payam_art,
            "armin-bethooven.com": armin_bethooven_com.armin_bethooven, "mehmoonivip.ir": mehmoonivip_ir.mehmoonivip,
            "iraniansound.com": iraniansound_com.iraniansound, "serenadepiano.ir": serenadepiano_ir.serenadepiano,
            "nimafereidooni.com": nimafereidooni_com.nimafereidooni, "navapiano.com": navapiano_com.navapiano,
            "gallery-chang.ir": gallery_chang_ir.gallery_chang, "rahavico.com": rahavico_com.rahavico,
            "mifado.ir": mifado_ir.mifado, "penzad.ir": penzad_ir.penzad,
            "www.sornagallery.com": www_sornagallery_com.sornagallery, "www.chare.ir": www_chare_ir.chare,
            "sornagallery.com": www_sornagallery_com.sornagallery, "www.onebazar.ir": www_onebazar_ir.onebazar,
            "honarahang.ir": honarahang_ir.honarahang, "shop.citymusic.ir": shop_citymusic_ir.shop_citymusic,
            "apadanamusic.ir": apadanamusic_ir.apadanamusic, "www.janasaz.com": www_janasaz_com.janasaz,
            "sedayemehr.com": sedayemehr_com.sedayemehr, "sazabzar.ir": sazabzar_ir.sazabzar,
            "www.avatatgostar.com": www_avatatgostar_com.avatatgostar, "itech.ir": itech_ir.itech,
            "solshop.ir": solshop_ir.solshop, "applecenter.ir": applecenter_ir.applecenter,
            "shahravamusic.ir": shahravamusic_ir.shahravamusic, "gadjets.ir": gadjets_ir.gadjets,
            "parsanme.com": parsanme_com.parsanme, "iranflute.com": iranflute_com.iranflute,
            "2sanie.com": twosanie_com.twosanie, "peskco.com": peskco_com.peskco,
            "www.mediaresan.com": www_mediaresan_com.mediaresan, "berimkharid.com": berimkharid_com.berimkharid,
            "camerashop.ir": camerashop_ir.camerashop, "miniatorcam.com": miniatorcam_com.miniatorcam,
            "sfone.ir": sfone_ir.sfone, "www.jibistore.com": www_jibistore_com.jibistore,
            "fav-co.com": fav_co_com.fav_co, "www.atramart.com": www_atramart_com.atramart,
            "ziadmiad.ir": ziadmiad_ir.ziadmiad, "phoneemdad.com": phoneemdad_com.phoneemdad,
            "www.modiseh.com": www_modiseh_com.modiseh, "rotbe1.ir": rotbe1_ir.rotbe1,
            "negahshot.com": negahshot_com.negahshot, "www.makanha.com": www_makanha_com.makanha,
            "audiox.ir": audiox_ir.audiox, "sazbox.com": sazbox_com.sazbox,
            "pst-iranian.ir": pst_iranian_ir.pst_iranian, "bodomarket.ir": bodomarket_ir.bodomarket,
            "tehranpioneer.com": tehranpioneer_com.tehranpioneer, "picenter.ir": picenter_ir.picenter,
            "alibababozorg.ir": alibababozorg_ir.alibababozorg, "www.dorbino.org": www_dorbino_org.dorbino,
            "shop.canon1.ir": shop_canon1_ir.shop_canon1, "www.irandeliver.com": www_irandeliver_com.irandeliver,
            "www.lensium.com": www_lensium_com.lensium, "focusnegar.com": focusnegar_com.focusnegar,
            "taktasvir.ir": taktasvir_ir.taktasvir, "digicenter.ir": digicenter_ir.digicenter,
            "rozanehshop.ir": rozanehshop_ir.rozanehshop, "miladcam.com": miladcam_com.miladcam,
            "falude.com": falude_com.falude, "arvandfm.com": arvandfm_com.arvandfm,
            "gariche.ir": gariche_ir.gariche, "mediastor.ir": mediastor_ir.mediastor,
            "k1land.com": k1land_com.k1land, "saazmarket.com": saazmarket_com.saazmarket,
            "www.pelazio.com": www_pelazio_com.pelazio, "abadimusic.com": abadimusic_com.abadimusic,
            "www.camshop.ir": www_camshop_ir.camshop, "paymishe.com": paymishe_com.paymishe,
            "royzkala.com": royzkala_com.royzkala, "basalam.com": basalam_com.basalam,
            "cameramarkazi.com": cameramarkazi_com.cameramarkazi, "www.edarikala.com": www_edarikala_com.edarikala,
            "pianomarket.ir": pianomarket_ir.pianomarket, "xn--ghbeb.com": xn__ghbeb_com.ghbeb,
            "melotiroj.academy": melotiroj_academy.melotiroj, "www.itbazar.com": www_itbazar_com.itbazar,
            "www.hamitak.com": www_hamitak_com.hamitak, "www.dingoland.ir": www_dingoland_ir.dingoland,
            "lenzocam.com": lenzocam_com.lenzocam, "tasvirkala.net": tasvirkala_net.tasvirkala,
            "sazhouse.com": www_sazhouse_com.sazhouse, "www.darvishkhan.net": www_darvishkhan_net.darvishkhan,
            "www.sazhouse.com": www_sazhouse_com.sazhouse, "sonorite.ir": sonorite_ir.sonorite,
            "hiapple.ir": hiapple_ir.hiapple, "gabri.ir": gabri_ir.gabri,
            "www.mobit.ir": www_mobit_ir.mobit, "filmkala.com": filmkala_com.filmkala,
            "www.iliyacomputer.com": www_iliyacomputer_com.iliyacomputer, "senfishop.com": senfishop_com.senfishop,
            "kandidshop.ir": kandidshop_ir.kandidshop, "technosun.ir": technosun_ir.technosun,
            "kalajibi.ir": www_kalajibi_ir.kalajibi, "matapoor.com": matapoor_com.matapoor,
            "www.kalajibi.ir": www_kalajibi_ir.kalajibi, "pubgdooni.com": pubgdooni_com.pubgdooni,
            "sazstore.com": sazstore_com.sazstore, "cafeguitar.ir": cafeguitar_ir.cafeguitar,
            "www.altontrading.com": www_altontrading_com.altontrading, "mobotools.ir": mobotools_ir.mobotools,
            "www.bazaryab.com": www_bazaryab_com.bazaryab, "parhammusic.ir": parhammusic_ir.parhammusic,
            "www.shop.musiccity.ir": www_shop_musiccity_ir.shop_musiccity, "proavl.net": proavl_net.proavl,
            "www.dokon.ir": www_dokon_ir.dokon, "yesjtd.rozblog.com": yesjtd_rozblog_com.yesjtd_rozblog,
            "offer.market": offer_market.offer_market, "afsharstore.com": afsharstore_com.afsharstore,
            "aria-mall.ir": aria_mall_ir.aria_mall, "sazcenter.com": sazcenter_com.sazcenter,
            "www.vafaiemusic.com": www_vafaiemusic_com.vafaiemusic, "timcheh.com": timcheh_com.timcheh,
            "shahab-store.com": shahab_store_com.shahab_store, "ofoghstore.ir": ofoghstore_ir.ofoghstore,
            "cinemakala.com": cinemakala_com.cinemakala, "kharidazma.com": kharidazma_com.kharidazma,
            "troly.ir": troly_ir.troly, "irandjstore.com": irandjstore_com.irandjstore,
            "www.parsian-sound.com": www_parsian_sound_com.parsian_sound, "persikav.com": persikav_com.persikav,
            "digibroadcast.ir": digibroadcast_ir.digibroadcast, "digionline.ir": digionline_ir.digionline,
            "elmond.ir": elmond_ir.elmond, "noahang.ir": noahang_ir.noahang,
            "sonystar.ir": sonystar_ir.sonystar, "rabi.ir": rabi_ir.rabi, "alimojood.ir": alimojood_ir.alimojood,
            "hitkala.ir": hitkala_ir.hitkala, "tasvirgostar.com": tasvirgostar_com.tasvirgostar,
            "alootop.com": alootop_com.alootop, "doorbin.store": doorbin_store.doorbin_store,
            "4sooo.com": four_sooo_com.four_sooo, "npdigi.com": npdigi_com.npdigi_com,
            "persiantopsound.com": persiantopsound_com.persiantopsound, "pianoforte.ir": pianoforte_ir.pianoforte,
            "qeshmkharid.ir": qeshmkharid_ir.qeshmkharid, "cafekhareed.com": cafekhareed_com.cafekhareed,
            "baniband.com": baniband_com.baniband, "didoshot.com": didoshot_com.didoshot,
            "sazamooz.com": sazamooz_com.sazamooz, "3710.ir": ir_3710.ir3710, "rabid.ir": rabid_ir.rabid,
            "aykalaa.ir": aykalaa_ir.aykalaa, "audioment.com": audioment_com.audioment,
            "www.uzmandigital.com": www_uzmandigital_com.uzmandigital, "royalvocal.com": royalvocal_com.royalvocal,
            "tehran-sote.com": tehran_sote_com.tehran_sote, "ecis.ir": ecis_ir.ecis,
            "solgallery.ir": solgallery_ir.solgallery, "meghdadit.com": meghdadit_com.meghdadit,
            "canonpersia.com": canonpersia_com.canonpersia, "kalafox.ir": kalafox_ir.kalafox,
            "www.rsa-co.com": www_rsa_co_com.rsa_co, "vizmarket.ir": vizmarket_ir.vizmarket,
            "yademanshop.ir": yademanshop_ir.yademanshop, "iraanbaba.com": iraanbaba_com.iraanbaba,
            "parsiankala.com": parsiankala_com.parsiankala_com, "www.tienda.ir": www_tienda_ir.tienda,
            "tasvirancam.ir": www_tasvirancam_ir.tasvirancam, "saazonline.ir": saazonline_ir.saazonline,
            "www.tasvirancam.ir": www_tasvirancam_ir.tasvirancam, "hbartarshop.com": hbartarshop_com.hbartarshop,
            "avazgar.com": avazgar_com.avazgar, "toptarin.net": toptarin_net.toptarin,
            "www.alphy-music.com": alphy_music_com.alphy_music, "torbatmelody.ir": torbatmelody_ir.torbatmelody,
            "alphy-music.com": alphy_music_com.alphy_music, "ertebat-sg.com": ertebat_sg_com.ertebat_sg,
            "parsiancredit.com": parsiancredit_com.parsiancredit, "irankurzweil.com": irankurzweil_com.irankurzweil,
            "electricomde.ir": electricomde_ir.electricomde, "www.cckala.com": www_cckala_com.cckala,
            "esfahanmelody.ir": esfahanmelody_ir.esfahanmelody, "arzoonyab.com": arzoonyab_com.arzoonyab,
            "shabakehstore.com": shabakehstore_com.shabakehstore, "gheimatnama.ir": gheimatnama_ir.gheimatnama,
            "www.erteash.ir": www_erteash_ir.erteash, "guitarhead.ir": guitarhead_ir.guitarhead,
            "bamakharid.com": bamakharid_com.bamakharid, "saazland.com": saazland_com.saazland,
            "inket.ir": inket_ir.inket, "toprayan.com": toprayan_com.toprayan, "dk99.ir": dk99_ir.dk99,
            "aref.ir": aref_ir.aref, "sedayenovin.ir": sedayenovin_ir.sedayenovin,
            "radek.ir": radek_ir.radek, "sazkhune.com": sazkhune_com.sazkhune,
            "musicsheida.com": musicsheida_com.musicsheida, "bavandpiano.com": bavandpiano_com.bavandpiano,
            "iransote.com": iransote_com.iransote, "iranloop.ir": iranloop_ir.iranloop,
            "www.iranloop.ir": iranloop_ir.iranloop, "behinmedia.ir": behinmedia_ir.behinmedia,
            "www.sazforoosh.com": www_sazforoosh_com.sazforoosh, "sazkala.com": sazkala_com.sazkala,
            "sedastore.com": sedastore_com.sedastore, "www.djcenter.net": www_djcenter_net.djcenter,
            "digiseda.ir": digiseda_ir.digiseda, "rayanseda.com": rayanseda_com.rayanseda,
            "sornashop.com": www_sornashop_com.sornashop, "gemamart.com": gemamart_com.gemamart,
            "www.sornashop.com": www_sornashop_com.sornashop, "davarmelody.com": davarmelody_com.davarmelody,
            "www.tehranmelody.com": www_tehranmelody_com.tehranmelody, "guitarbaz.com": guitarbaz_com.guitarbaz_com,
            "tehranmelody.software": www_tehranmelody_com.tehranmelody, "pianocenter.ir": pianocenter_ir.pianocenter,
            "www.golhastore.ir": golhastore_ir.golhastore, "www.abarbazar.com": www_abarbazar_com.abarbazar,
            "navamarket.ir": navamarket_ir.navamarket, "golhastore.ir": golhastore_ir.golhastore,
            "ertebat.co": ertebat_co.ertebat, "delshadmusic.com": delshadmusic_com.delshadmusic,
            "delarammusic.com": delarammusic_com.delarammusic, "alikmusic.org": alikmusic_org.alikmusic,
            "violincenter.ir": violincenter_ir.violincenter, "donyayesazha.com": donyayesazha_com.donyayesazha,
            "sedabazar.com": sedabazar_com.sedabazar, "www.hezarsoo.com": www_hezarsoo_com.hezarsoo,
            "fluteshop.org": fluteshop_org.fluteshop, "digitalbaran.com": digitalbaran_com.digitalbaran,
            "turingsanat.com": turingsanat_com.turingsanat, "yerial.com": yerial_com.yerial,
            "www.gostaresh-seda.com": www_gostaresh_seda_com.gostaresh, "headroom.ir": headroom_ir.headroom,
            "www.digikala.com": www_digikala_com.digikala, "malihshop.ir": malihshop_ir.malihshop,
            "beyerdynamic-iran.com": beyerdynamic_iran_com.beyerdynamic, "sazplaza.com": www_sazplaza_com.sazplaza,
            "www.sazplaza.com": www_sazplaza_com.sazplaza, "www.kalaoma.com": www_kalaoma_com.kalaoma,
            "jahanmelody.com": jahanmelody_com.jahanmelody, "echokowsar.com": echokowsar_com.echokowsar,
            "sotplus.ir": sotplus_ir.sotplus, "noornegar.com": noornegar_com.noornegar,
            "www.artemusic.ir": www_artemusic_ir.artemusic, "dgland.com": dgland_com.dgland,
            "saaz24.com": saaz24_com.saaz24, "melodinng.com": melodinng_com.melodinng,
            "www.afrangdigital.com": www_afrangdigital_com.afrangdigital, "bangino.ir": bangino_ir.bangino,
            "parsiansote.com": parsiansote_com.parsiansote, "emalls.ir": emalls_ir.emalls,
            "technicav.com": technicav_com.technicav, "www.didnegar.com": www_didnegar_com.didnegar,
            "www.alijavadzadeh.com": www_alijavadzadeh_com.alijavadzadeh, "bia2piano.ir": bia2piano_ir.bia2piano,
            "sedamoon.com": sedamoon_com.sedamoon, "malltina.com": malltina_com.malltina,
            "pishgaman-seda.com": pishgaman_seda_com.pishgaman, "www.dourbinet.com": www_dourbinet_com.dourbinet,
            "avatasvir.com": avatasvir_com.avatasvir, "hilatel.ir": hilatel_ir.hilatel,
            "www.yamahairan.ir": www_yamahairan_ir.yamahairan, "yamahairan.ir": www_yamahairan_ir.yamahairan,
            "navakade.com": navakade_com.navakade, "santoorsadeghi.com": santoorsadeghi_com.santoorsadeghi,
            "head-phone.ir": head_phone_ir.head_phone, "touchmusic.ir": touchmusic_ir.touchmusic,
            "www.ghesticlub.com": www_ghesticlub_com.ghesticlub, "pcmaxhw.com": pcmaxhw_com.pcmaxhw,
            "www.pixel.ir": www_pixel_ir.pixel, "www.bokehland.com": www_bokehland_com.bokehland,
            "hajigame.ir": hajigame_ir.hajigame, "janebi.com": janebi_com.janebi,
            "jeddikala.com": jeddikala_com.jeddikala, "didbartarshop.ir": didbartarshop_ir.didbartarshop,
            "max-shop.ir": max_shop_ir.max_shop, "www.pakhsh.shop": www_pakhsh_shop.pakhsh,
            "www.safirkala.com": www_safirkala_com.safirkala, "namacam.ir": namacam_ir.namacam,
            "www.akasisaatchi.com": www_akasisaatchi_com.akasisaatchi, "www.flashiran.net": fluteshop_org.fluteshop,
            "mehragin.com": mehragin_com.mehragin, "barbadgallery.com": barbadgallery_com.barbadgallery,
            "zirpele.ir": zirpele_ir.zirpele, "parsacam.com": parsacam_com.parsacam,
            "negahshop.com": negahshop_com.negahshop, "didgahstore.ir": didgahstore_ir.didgahstore,
            "chavoosh110.com": chavoosh110_com.chavoosh110, "edbazar.com": edbazar_com.edbazar,
            "saz-bazar.com": saz_bazar_com.saz_bazar, "mahancamera.com": mahancamera_com.mahancamera,
            "avazac.com": avazac_com.avazac, "exif.ir": exif_ir.exif, "diddovom.com": diddovom_com.diddovom,
            "classicshopper.ir": classicshopper_ir.classicshopper, "golden8.ir": golden8_ir.golden8,
            "logilook.com": logilook_com.logilook, "lioncomputer.com": lioncomputer_com.lioncomputer,
            "www.lioncomputer.com": lioncomputer_com.lioncomputer, "glorytar.com": glorytar_com.glorytar,
            "bobloseven.com": bobloseven_com.bobloseven, "kingbrand.ir": kingbrand_ir.kingbrand,
            "www.kingbrand.ir": kingbrand_ir.kingbrand, "egerd.com": egerd_com.egerd,
            "jskala.com": jskala_com.jskala, "asarayan.com": asarayan_com.asarayan,
            "tehranspeaker.com": tehranspeaker_com.tehranspeaker, "sazkade.com": sazkade_com.sazkade,
            "www.tehranspeaker.com": tehranspeaker_com.tehranspeaker, "audionovin.com": audionovin_com.audionovin,
            "www.technolife.ir": technolife_ir.technolife, "digiarki.com": digiarki_com.digiarki,
            "technolife.ir": technolife_ir.technolife, "www.pro-av.ir": www_pro_av_ir.pro_av,
            "www.zanbil.ir": zanbil_ir.zanbil, "musicalshop.ir": musicalshop_ir.musicalshop,
            "mahgoni.com": mahgoni_com.mahgoni, "zanbil.ir": zanbil_ir.zanbil, "gilsara.com": gilsara_com.gilsara,
            "esam.ir": esam_ir.esam, "bahartak.ir": bahartak_ir.bahartak, "mahor.net": mahor_net.mahor,
            "torob.com": torob_com.torob, "arads.ir": arads_ir.arads, "www.dodoak.com": www_dodoak_com.dodoak,
            "yamahakerman.ir": yamahakerman_ir.yamahakerman, "tehranseda.com": tehranseda_com.tehranseda,
            "www.ava-avl.com": www_ava_avl_com.ava_avl, "kalastudio.ir": kalastudio_ir.kalastudio,
            "pianopars.ir": pianopars_ir.pianopars, "www.kalands.ir": www_kalands_ir.kalands,
            "www.seda.center": seda_center.seda_center, "echista.ir": echista_ir.echista,
            "www.brilliantsound.ir": www_brilliantsound_ir.brilliantsound, "seda.center": seda_center.seda_center,
            "www.sedatasvir.com": www_sedatasvir_com.sedatasvir, "guitarcity.ir": guitarcity_ir.guitarcity,
            "sazzbazz.com": sazzbazz_com.sazzbazz, "seda.market": seda_market.seda_market,
            "laranet.ir": laranet_ir.laranet, "iranheadphone.com": iranheadphone_com.iranheadphone,
            "iranfender.com": iranfender_com.iranfender, "www.solbemol.com": www_solbemol_com.solbemol,
            "guitariran.com": guitariran_com.guitariran, "notehashtom.ir": notehashtom_ir.notehashtom,
            "sazclub.com": sazclub_com.sazclub, "parseda.com": parseda_com.parseda,
            "top-headphone.com": top_headphone_com.top_headphone, "sazbazzar.com": sazbazzar_com.sazbazzar,
            "www.guitar-center.ir": www_guitar_center_ir.guitar_center, "studiopaya.com": studiopaya_com.studiopaya,
            "musickala.com": musickala_com.musickala, "soatiran.com": soatiran_com.soatiran,
            "irofferr.ir": irofferr_ir.irofferr, "tehrandj.com": tehrandj_com.tehrandj,
            "sowtazhang.ir": sowtazhang_ir.sowtazhang, "andalosmusic.com": andalosmusic_com.andalosmusic,
            "barbadpiano.com": barbadpiano_com.barbadpiano, "neynava-store.com": neynava_store_com.neynava_store,
            "sotecenter.com": sotecenter_com.sotecenter, "avaparsian.com": avaparsian_com.avaparsian,
            "www.shiraz-beethoven.ir": shiraz_beethoven_ir.shiraz_beethoven,
            "shiraz-beethoven.ir": shiraz_beethoven_ir.shiraz_beethoven, "musicala.ir": musicala_ir.musicala,
            "shabahang.shop": shabahang_shop.shabahang, "golhastore.com": golhastore_com.golhastore,
            "www.shabahangmusic.com": www_shabahangmusic_com.shabahangmusic, "diafoto.ir": diafoto_ir.diafoto,
            "www.avancomputer.com": www_avancomputer_com.avancomputer_com, "payatel.com": payatel_com.payatel,
            "arasound.ir": arasound_ir.arasound, "shahresaz.com": shahresaz_com.shahresaz,
            "arshiamehr.co": arshiamehr_co.arshiamehr, "tehransaz.com": tehransaz_com.tehransaz,
            "kharidkala24.com": kharidkala24_com.kharidkala24, "dorbino.org": dorbino_org.dorbino,
            "saazestaan.com": saazestaan_com.saazestaan, "www.zhovanmusic.com": zhovanmusic_com.zhovanmusic,
            "sinacamera.ir": sinacamera_ir.sinacamera, "turborayan.com": turborayan_com.turborayan,
            "www.ghestico.com": ghestico_com.ghestico, "zhiyunkala.com": zhiyunkala_com.zhiyunkala,
            "m3sell.com": m3sell_com.m3sell, "santoorsadeghi.ir": santoorsadeghi_ir.santoorsadeghi,
            "canon1.ir": canon1_ir.canon1, "memorybazar.com": memorybazar_com.memorybazar,
            "www.rayanmusic.com": rayanmusic_com.rayanmusic, "nobesho.com": nobesho_com.nobesho,
            "1xmarket.com": www_1xmarket_com.www_1xmarket, "nooracam.com": nooracam_com.nooracam,
            "beethovenmshop.com": beethovenmshop_com.beethovenmshop, "www.agrastore.ir": www_agrastore_ir.agrastore,
            "www.mahdigit.ir": mahdigit_ir.mahdigit, "www.khaneyesaaz.ir": www_khaneyesaaz_ir.khaneyesaaz,
            "sazplus.com": sazplus_com.sazplus, "saazaar.com": saazaar_com.saazaar,
            "papiran.ir": papiran_ir.papiran, "activemarket24.com": activemarket24_com.activemarket24,
            "www.sazbebar.com": www_sazbebar_com.sazbebar, "dragon-shop.ir": dragon_shop_ir.dragon_shop,
            "saazbaaz.com": saazbaaz_com.saazbaaz,"doornegahshop.com":doornegahshop_com.doornegahshop,
            "microless_ir": microless_ir.microless}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}


def callCrawlerThread(link, site, statistic, total):
    import datetime
    statistic['TOTAL'] = statistic['TOTAL'] + 1
    # config.lastCrawlEnded = 'running ' + str(statistic['TOTAL'])
    config.lastCrawlEnded = 'running ' + "{0:.3f}%".format((statistic['TOTAL'] * 100) / total)
    # print('running ', statistic['TOTAL'])
    logger = logging.getLogger(__name__)
    time.sleep(2 + random.randint(1, 5))
    link = Link.objects.get(id=link['id'])
    start_time = time.time()
    link.last_run_started = datetime.datetime.now()
    link.save()
    try:
        product = crawlers[site[0]](link, headers, site[0])
    except Exception as e:
        logger.info('%s %s :  %s,', "{0:.2f}s".format((time.time() - start_time)), str(link.id), e)
        link.last_run = -2
        link.last_run_ended = datetime.datetime.now()
        link.save()
        return

    if product is None:
        logger.info('%s, null :  %s,', "{0:.2f}s".format((time.time() - start_time)), site[0])
        link.last_run = -1
        link.last_run_ended = datetime.datetime.now()
        link.save()
        return
    duration = time.time() - start_time

    if site[0] not in statistic:
        statistic[site[0]] = {"count": 0, "total": duration}
    else:
        statistic[site[0]] = {
            "count": statistic[site[0]]["count"] + 1,
            "total": statistic[site[0]]["total"] + duration
        }
    if product == 0:
        product = -1
    link.last_run = math.ceil(time.time() - start_time)
    link.last_run_ended = datetime.datetime.now()
    link.save()
    updateLink(link, product, site[0])


crawlersFast = {"torob.com": torob_com.torob, "emalls.ir": emalls_ir.emalls,
                "iranloop.ir": iranloop_ir.iranloop, "golhastore.ir": golhastore_ir.golhastore,
                "www.sazforoosh.com": www_sazforoosh_com.sazforoosh}


def callCrawlerThreadFast(link, site, i):
    config.lastCrawlEnded = 'running ' + str(i)
    try:
        product = crawlersFast[site[0]](link, headers, site[0])
    except Exception as e:
        print(e)
        return

    if product is None:
        print("None")
        return

    if product == 0:
        product = -1
    print("product ", product)
    updateLink(link, product)


def updateLink(link, product, site):
    lastPrice = Price.objects.filter(parent=link).order_by('-created').first()
    if lastPrice is None or lastPrice.value != product:
        try:
            price = Price.objects.create(parent=link)
            price.value = product
            if site != 'divar.ir':
                link.unseen = True
                musicItem = MusicItem.objects.get(pk=link.parent_id)
                if price.value == -1:
                    musicItem.out_of_stock += 1
                elif lastPrice is None or (lastPrice.value != -1 and lastPrice.value < price.value):
                    musicItem.increase += 1
                elif lastPrice.value == -1:
                    musicItem.in_stock += 1
                else:
                    musicItem.decrease += 1
                musicItem.save()
                config.lastCrawlChanges += 1
            price.save()
            link.save()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.info('%s', e)


def reloadMusicItemPrice(item, i):
    time.sleep(1 + random.randint(0, 1))
    price = www_donyayesaaz_com.donyayesaaz(item.url, headers)
    item.price = price
    item.save()
    return


def test_link(url):
    class Object(object):
        pass

    a = Object()
    a.url = url
    site = re.findall("//(.*?)/", a.url)
    return crawlers[site[0]](a, headers, site[0])


def manualBrowse():
    links = Link.objects.all()
    for i in range(0, len(links)):
        link = links[i]
        lastPrice = Price.objects.filter(parent=link).order_by('-created').first()
        try:
            if lastPrice is None:
                print(str(i), " None ", link.url)
            else:
                print(str(i), " ", str(lastPrice.value), " ", link.url)
            chrome_options = Options()
            chrome_options.add_argument('log-level=3')
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)
            driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), options=chrome_options)
            driver.get(link.url)
            while True:
                driver.title
                time.sleep(1)
        except:
            continue

# testData = [
#     {"name": "alikmusic.org", "links": [
#         {"value": 45600000,
#          "url": "https://alikmusic.org/newalik/product/%d9%be%db%8c%d8%a7%d9%86%d9%88-%d8%af%db%8c%d8%ac%db%8c%d8%aa%d8%a7%d9%84-%da%a9%d8%a7%d8%b3%db%8c%d9%88-px770-bk/"},
#         {"value": 15000000,
#          "url": "https://alikmusic.org/newalik/product/%d9%87%d9%86%da%af-%d8%af%d8%b1%d8%a7%d9%85-%da%a9%db%8c%d8%aa%d8%a7-9-%d9%86%d8%aa/"},
#         {"value": -1,
#          "url": "https://alikmusic.org/newalik/product/%da%af%db%8c%d8%aa%d8%a7%d8%b1-%d9%be%d8%a7%d8%b1%d8%b3%db%8c-m1/"},
#         {"value": -1, "url": "https://alikmusic.org/newalik/product/alhambra-3c/"}
#     ]},
#     {"name": "alootop.com", "links": [
#         {"value": 409000,
#          "url": "https://alootop.com/product/%d8%a7%d8%b3%d9%be%db%8c%da%a9%d8%b1-awei-y336-%d8%b6%d8%af-%d8%a2%d8%a8/"},
#         {"value": 449000,
#          "url": "https://alootop.com/product/%d9%87%d8%af%d8%b3%d8%aa-%d8%a7%da%a9%d8%b3%d9%88%d9%86-gh-11-%da%af%db%8c%d9%85%db%8c%d9%86%da%af/"},
#         {"value": -1,
#          "url": "https://alootop.com/product/%da%a9%db%8c%d8%a8%d9%88%d8%b1%d8%af-%d8%aa%d8%b3%da%a9%d9%88-tk-8011/"}
#     ]},
#     {"name": "alphy-music.com", "links": [
#         {"value": 22000000, "url": "https://alphy-music.com/shop/product/10-porsche-carrera-4964.html"},
#         {"value": 1660000,
#          "url": "https://alphy-music.com/shop/product/233-%D9%85%DB%8C%D8%AF%DB%8C-%DA%A9%D9%86%D8%AA%D8%B1%D9%84%D8%B1-m-audio-oxygen-25-vi.html"}
#     ]},
#     {"name": "arads.ie", "links": [
#         {"value": 29000,
#          "url": "https://arads.ir/product/5819228/%D9%BE%DB%8C%DA%A9-%DA%AF%DB%8C%D8%AA%D8%A7%D8%B1-%D8%AF%D8%A7%D8%AF%D8%A7%D8%B1%DB%8C%D9%88-%D9%85%D8%AF%D9%84-nylpro14"},
#         {"value": -1,
#          "url": "https://arads.ir/product/12432/%D8%A7%D8%AA%D9%88-%D9%85%D8%AE%D8%B2%D9%86-%D8%AF%D8%A7%D8%B1-%D9%81%DB%8C%D9%84%DB%8C%D9%BE%D8%B3-%D9%85%D8%AF%D9%84-gc6802"}
#     ]},
#     {"name": "aref.ir", "links": [
#         {"value": 2050000,
#          "url": "https://aref.ir/product/%d8%b3%d9%86%d8%aa%d9%88%d8%b1-%d9%81%d8%b1%d9%87%d8%a7%d8%af-%d8%af%d8%b1%d8%ac%d9%87-1/"},
#         {"value": -1,
#          "url": "https://aref.ir/product/%da%af%db%8c%d8%aa%d8%a7%d8%b1-%d8%b1%d9%88%d9%85%d8%a8%d8%a7-rhumba/"}
#     ]},
#     {"name":"arzoonyab.com","links":[
#         {"value":86900000,"url":"https://arzoonyab.com/item/?iid=6725_5124"},
#         {"value":}
#     ]}
# ]
#
#
# def unitTest():
#     import re
#     for test in testData:
#         problem = False
#         for link in test["links"]:
#             site = re.findall("//(.*?)/", link["url"])
#             try:
#                 class Object(object):
#                     pass
#
#                 a = Object()
#                 a.url = link["url"]
#                 product = crawlers[site[0]](a, headers, site[0])
#                 if product != link["value"]:
#                     problem = True
#                     break
#             except Exception as e:
#                 problem = True
#                 break
#         if problem:
#             print(test["name"], "failed")
#         else:
#             print(test["name"], "pass")
