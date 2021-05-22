import logging
import time
from models.models import Price, Link, MusicItem
from constance import config
from models.crawlers import *
import random

crawlers = {"hitkala.ir": hitkala_ir.hitkala, "tasvirgostar.com": tasvirgostar_com.tasvirgostar,
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
            "www.tasvirancam.ir": www_tasvirancam_ir.tasvirancam, "hbartarshop.com": hbartarshop_com.hbartarshop,
            "avazgar.com": avazgar_com.avazgar, "toptarin.net": toptarin_net.toptarin,
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
            "www.sazforoosh.com": www_sazforoosh_com.sazforoosh, "sazkala.com": sazkala_com.sazkala,
            "sedastore.com": sedastore_com.sedastore, "www.djcenter.net": www_djcenter_net.djcenter,
            "digiseda.ir": www_djcenter_net.djcenter, "rayanseda.com": rayanseda_com.rayanseda,
            "www.sornashop.com": www_sornashop_com.sornashop, "davarmelody.com": davarmelody_com.davarmelody,
            "www.tehranmelody.com": www_tehranmelody_com.tehranmelody, "guitarbaz.com": guitarbaz_com.guitarbaz_com,
            "tehranmelody.software": www_tehranmelody_com.tehranmelody,
            "navamarket.ir": navamarket_ir.navamarket, "golhastore.ir": golhastore_ir.golhastore,
            "ertebat.co": ertebat_co.ertebat, "delshadmusic.com": delshadmusic_com.delshadmusic,
            "delarammusic.com": delarammusic_com.delarammusic, "alikmusic.org": alikmusic_org.alikmusic,
            "violincenter.ir": violincenter_ir.violincenter, "donyayesazha.com": donyayesazha_com.donyayesazha,
            "sedabazar.com": sedabazar_com.sedabazar, "www.hezarsoo.com": www_hezarsoo_com.hezarsoo,
            "fluteshop.org": fluteshop_org.fluteshop, "digitalbaran.com": digitalbaran_com.digitalbaran,
            "turingsanat.com": turingsanat_com.turingsanat, "yerial.com": yerial_com.yerial,
            "www.gostaresh-seda.com": www_gostaresh_seda_com.gostaresh,
            "www.digikala.com": www_digikala_com.digikala, "malihshop.ir": malihshop_ir.malihshop,
            "beyerdynamic-iran.com": beyerdynamic_iran_com.beyerdynamic,
            "www.sazplaza.com": www_sazplaza_com.sazplaza, "www.kalaoma.com": www_kalaoma_com.kalaoma,
            "jahanmelody.com": jahanmelody_com.jahanmelody, "echokowsar.com": echokowsar_com.echokowsar,
            "sotplus.ir": sotplus_ir.sotplus, "noornegar.com": noornegar_com.noornegar,
            "www.artemusic.ir": www_artemusic_ir.artemusic, "dgland.com": dgland_com.dgland,
            "saaz24.com": saaz24_com.saaz24, "melodinng.com": melodinng_com.melodinng,
            "www.afrangdigital.com": www_afrangdigital_com.afrangdigital,
            "parsiansote.com": parsiansote_com.parsiansote, "emalls.ir": emalls_ir.emalls,
            "technicav.com": technicav_com.technicav, "www.didnegar.com": www_didnegar_com.didnegar,
            "www.alijavadzadeh.com": www_alijavadzadeh_com.alijavadzadeh, "bia2piano.ir": bia2piano_ir.bia2piano,
            "sedamoon.com": sedamoon_com.sedamoon, "malltina.com": malltina_com.malltina,
            "pishgaman-seda.com": pishgaman_seda_com.pishgaman, "www.dourbinet.com": www_dourbinet_com.dourbinet,
            "avatasvir.com": avatasvir_com.avatasvir, "hilatel.ir": hilatel_ir.hilatel,
            "www.yamahairan.ir": www_yamahairan_ir.yamahairan, "yamahairan.ir": www_yamahairan_ir.yamahairan,
            "navakade.com": navakade_com.navakade,
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
            "www.lioncomputer.com": lioncomputer_com.lioncomputer,
            "bobloseven.com": bobloseven_com.bobloseven, "kingbrand.ir": kingbrand_ir.kingbrand,
            "www.kingbrand.ir": kingbrand_ir.kingbrand, "egerd.com": egerd_com.egerd,
            "jskala.com": jskala_com.jskala, "asarayan.com": asarayan_com.asarayan,
            "tehranspeaker.com": tehranspeaker_com.tehranspeaker, "sazkade.com": sazkade_com.sazkade,
            "www.tehranspeaker.com": tehranspeaker_com.tehranspeaker, "audionovin.com": audionovin_com.audionovin,
            "technolife.ir": technolife_ir.technolife, "www.pro-av.ir": www_pro_av_ir.pro_av,
            "mahgoni.com": mahgoni_com.mahgoni, "zanbil.ir": zanbil_ir.zanbil, "gilsara.com": gilsara_com.gilsara,
            "esam.ir": esam_ir.esam, "bahartak.ir": bahartak_ir.bahartak, "mahor.net": mahor_net.mahor,
            "torob.com": torob_com.torob, "arads.ir": arads_ir.arads, "www.dodoak.com": www_dodoak_com.dodoak,
            "yamahakerman.ir": yamahakerman_ir.yamahakerman, "tehranseda.com": tehranseda_com.tehranseda,
            "www.ava-avl.com": www_ava_avl_com.ava_avl, "kalastudio.ir": kalastudio_ir.kalastudio,
            "pianopars.ir": pianopars_ir.pianopars, "www.kalands.ir": www_kalands_ir.kalands,
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
            "shiraz-beethoven.ir": shiraz_beethoven_ir.shiraz_beethoven, "musicala.ir": musicala_ir.musicala,
            "shabahang.shop": shabahang_shop.shabahang,
            "www.shabahangmusic.com": www_shabahangmusic_com.shabahangmusic}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}


def callCrawlerThread(link, site, i, statistic):
    statistic['TOTAL'] = statistic['TOTAL'] + 1
    config.lastCrawlEnded = 'running ' + str(statistic['TOTAL'])
    print('running ', statistic['TOTAL'])
    logger = logging.getLogger(__name__)
    time.sleep(2 + random.randint(1, 5))
    start_time = time.time()
    try:
        product = crawlers[site[0]](link, headers, site[0])
    except Exception as e:
        logger.info('%s %s :  %s,', "{0:.2f}s".format((time.time() - start_time)), str(i), site[0])
        return

    if product is None:
        logger.info('%s, null :  %s,', "{0:.2f}s".format((time.time() - start_time)), site[0])
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
    updateLink(link, product)


def updateLink(link, product):
    lastPrice = Price.objects.filter(parent=link).order_by('-created').first()
    if lastPrice is None or lastPrice.value != product:
        try:
            price = Price.objects.create(parent=link)
            price.value = product
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
            price.save()
            link.save()
            config.lastCrawlChanges += 1
        except Exception as e:
            logger.info('%s', e)


def reloadMusicItemPrice(item, i):
    time.sleep(1 + random.randint(0, 1))
    price = www_donyayesaaz_com.donyayesaaz(item.url, headers)
    item.price = price
    item.save()
    config.lastCrawlEnded = 'loading ' + str(i)
    return
