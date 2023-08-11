import {
  For,
  Index,
  Show,
  Suspense,
  createResource,
  createSignal,
} from "solid-js";
import LoadingScreen from "../containers/LoadingScreen";
import Header from "../containers/Header";
// import data from "@/data/EdanMeyerVpt_scrolltl_qaresult.json";
// import data from "@/data/IEEEVR2022Ogawa_scrolltl_qaresult.json";

const qaResultPlotsDispTargets = [
  "mse",
  "ssim",
  "psnr",
  "hist_bin",
  "h_pp_coeff",
  "v_pp_coeff",
];

const loadData = async (asset_id) => {
  // const path = "@/data/IEEEVR2022Ogawa_scrolltl_qaresult.json";
  return (await import(`@/data/${asset_id}_scrolltl_qaresult.json`)).default;
};

const loadPlots = async (asset_id) => {
  const images = {};

  for (const target of qaResultPlotsDispTargets) {
    console.log(target);
    images[target] = (
      await import(`@/data/${asset_id}_${target}_plot.png`)
    ).default;
  }

  return images;
};

type AssetId = "EdanMeyerVpt" | "IEEEVR2022Ogawa";

export default function Home() {
  // console.log(data);
  const [assetId, setAssetId] = createSignal<AssetId>("IEEEVR2022Ogawa");
  const [data, info_data] = createResource(assetId, loadData);
  const [plots, info_plots] = createResource(assetId, loadPlots);

  const handleClickAssetSelector = (e) => setAssetId(e.target.innerText);

  return (
    <>
      <Suspense fallback={<LoadingScreen />}>
        <div>
          <Header
            assetId={assetId()}
            handleClickAssetSelector={handleClickAssetSelector}
          />
          {/* <header class="flex gap-2 justify-between text-2xl p-2 shadow-lg sticky top-0 bg-slate-200">
            <h1 class="flex gap-2 items-center">
              Showing: <b>{assetId()}</b>
            </h1>
            <div class="flex gap-2 justify-center font-bold">
              <button
                class="rounded-md shadow-md bg-slate-600 text-white p-2"
                onClick={handleClickAssetSelector}
              >
                EdanMeyerVpt
              </button>
              <button
                class="rounded-md shadow-md bg-slate-600 text-white p-2"
                onClick={handleClickAssetSelector}
              >
                IEEEVR2022Ogawa
              </button>
            </div>
          </header> */}
          <div class="px-2 py-16 bg-slate-300">
            <h2 class="text-center text-xl font-bold">Results Summary</h2>
            <div class={`grid gap-2 grid-cols-3`}>
              <Show when={plots()}>
                <For each={qaResultPlotsDispTargets}>
                  {(qakey) => <img class="w-full" src={plots()[qakey]} />}
                </For>
              </Show>
            </div>
          </div>

          <h2 class="text-center text-xl font-bold">Details</h2>
          <For each={data()}>
            {(item) => (
              <div class="mb-10 p-4 border-1 shadow-md w-[90%] mx-auto rounded-md">
                <div class="flex gap-2 p-2">
                  <div class="grid gap-2 w-1/3">
                    <img class="w-full shadow-md" src={item.im_frame[1]} />
                    <p class="text-center font-bold">video frame snapshot</p>
                    <p class="text-center font-bold">
                      {item.im_frame[0][1]} x {item.im_frame[0][0]} , channels=
                      {item.im_frame[0][2]}
                    </p>
                  </div>
                  <div class="grid gap-2 w-1/3">
                    <img class="w-full shadow-md" src={item.im_matched[1]} />
                    <p class="text-center font-bold">match result</p>
                    <p class="text-center font-bold">
                      {item.im_matched[0][1]} x {item.im_matched[0][0]} ,
                      channels=
                      {item.im_matched[0][2]}
                    </p>
                  </div>
                  <div class="grid gap-2 w-1/3">
                    <img class="w-full shadow-md" src={item.im_diff[1]} />
                    <p class="text-center font-bold">absdiff</p>
                    <p class="text-center font-bold">
                      {item.im_diff[0][1]} x {item.im_diff[0][0]} , channels=1
                    </p>
                  </div>
                </div>
                <p class="text-center text-2xl">time : {item.frame_time}</p>
                <div class="h-4"></div>
                {qaResultPlotsDispTargets.map((key) => (
                  <p class="text-2xl flex gap-4 justify-center">
                    {key} : {item.qa_result[key]}
                    {/* {item.qa_result[key]map((v) => (
                    <span>{v}</span>
                  ))} */}
                  </p>
                ))}
                <div class="h-4"></div>
                <p class="text-2xl flex gap-4 justify-center">
                  hist_bgr (b, g, r):
                  {item.qa_result.hist_bgr.map((v, i) => (
                    <span>
                      {["b", "g", "r"][i]} = {v}
                    </span>
                  ))}
                </p>
              </div>
            )}
          </For>
        </div>
      </Suspense>
    </>
  );
}
