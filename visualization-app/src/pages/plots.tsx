import { For, Index, Suspense, createResource, createSignal } from "solid-js";
import LoadingScreen from "../containers/LoadingScreen";
// import data from "@/data/EdanMeyerVpt_scrolltl_qaresult.json";
// import data from "@/data/IEEEVR2022Ogawa_scrolltl_qaresult.json";

const loadData = async (asset_id) => {
  // const path = "@/data/IEEEVR2022Ogawa_scrolltl_qaresult.json";
  return (await import(`@/data/${asset_id}_scrolltl_qaresult.json`)).default;
};

type AssetId = "EdanMeyerVpt" | "IEEEVR2022Ogawa";

export default function Home() {
  // console.log(data);
  const [assetId, setAssetId] = createSignal<AssetId>("IEEEVR2022Ogawa");
  const [data, info] = createResource(assetId, loadData);

  const handleClickAssetSelector = (e) => setAssetId(e.target.innerText);

  return (
    <>
      <Suspense fallback={<LoadingScreen />}>
        <div>
          <header class="flex gap-2 justify-between text-2xl p-2 shadow-lg sticky top-0 bg-slate-200">
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
          </header>
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
                <p class="text-2xl flex gap-4 justify-center">
                  ssim : {item.qa_result.ssim}
                  {/* {item.qa_result.ssim.map((v) => (
                    <span>{v}</span>
                  ))} */}
                </p>
                <p class="text-2xl flex gap-4 justify-center">
                  psnr : {item.qa_result.psnr}
                  {/* {item.qa_result.psnr.map((v) => (
                    <span>{v}</span>
                  ))} */}
                </p>
                <p class="text-2xl flex gap-4 justify-center">
                  mse : {item.qa_result.mse}
                  {/* {item.qa_result.psnr.map((v) => (
                    <span>{v}</span>
                  ))} */}
                </p>
                {/* <p class="text-2xl flex gap-4 justify-center">
                  gmsd : {item.qa_result.gmsd}
                  {item.qa_result.gmsd.map((v) => (
                    <span>{v}</span>
                  ))}
                </p> */}
                <p class="text-2xl flex gap-4 justify-center">
                  hist_bgr (b, g, r):
                  {item.qa_result.hist_bgr.map((v, i) => (
                    <span>
                      {["b", "g", "r"][i]} = {v}
                    </span>
                  ))}
                </p>
                <p class="text-2xl flex gap-4 justify-center">
                  hist_bin: {item.qa_result.hist_bin}
                </p>
              </div>
            )}
          </For>
        </div>
      </Suspense>
    </>
  );
}
