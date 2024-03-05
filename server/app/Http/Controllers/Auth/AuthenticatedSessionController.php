<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use App\Http\Requests\Auth\LoginRequest;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

use Illuminate\Support\Facades\Auth;

class AuthenticatedSessionController extends Controller
{
    /**
     * Handle an incoming authentication request.
     */
    public function store(LoginRequest $request): JsonResponse
    {
        $request->authenticate();

        // $request->session()->regenerate();

        $token = $request->user()->createToken($request->user()->email);

        return response()->json(['token' => $token->plainTextToken]);
    }

    /**
     * Destroy an authenticated session.
     */
    public function destroy(Request $request): JsonResponse
    {
        try {
            Auth::guard('web')->logout();
            $request->user()->currentAccessToken()->delete();
            $request->session()->regenerate();
        } catch (\Throwable $th) {
            //throw $th;
        }

        return response()->json(['status' => "success"]);
    }
}
